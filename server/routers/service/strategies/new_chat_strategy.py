import uuid
from uuid import UUID
import json
from datetime import datetime, timezone
from typing import List, Dict

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from routers.models.models import engine, sync_engine, User, ChatHistory, Message
from openai import AsyncOpenAI

from .base_chat_strategy import BaseChatStrategy, ChatRequest


class NewChatStrategy(BaseChatStrategy):
    """类"""
    async def chat_init(self):
        """对话初始化以及基本基础操作"""
        self.chat_request.chat_id = str(UUID)
        user_id = self.request.session.get("user").get("authed_user_id")
        user_uuid = self.request.session.get("user").get("authed_user_uuid")
        # 新建对话记录并保存用户消息
        async with self.db.begin():
            # 新建并保存对话记录
            chat_history = ChatHistory(
                chat_id=self.chat_request.chat_id,
                chat_topic=self.chat_request.user_message[:32],
                user_id=user_id,
                user_uuid=user_uuid,
            )
            self.db.add(chat_history)
            # 保存用户消息
            user_message = Message(
                message_id=self.chat_request.message_id,
                message_role="user",
                message_content=self.chat_request.user_message,
                chat_id=self.chat_request.chat_id
            )
            self.db.add(user_message)
            await self.db.commit()

    async def build_chat_context(self, chat_id: UUID) -> List[Dict]:
        """
        构建对话上下文
        """
        result = await self.db.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.timestamp.asc())
        )
        messages = result.scalars().all()
        # 转换消息格式并维护角色交替
        context = []
        last_role = None
        for msg in messages:
            if msg.message_role == last_role:
                # 合并连续相同角色的消息
                context[-1]["content"] += "\n" + msg.message_content
            else:
                context.append({
                    "role": msg.message_role,
                    "content": msg.message_content
                })
                last_role = msg.message_role
        return context

    async def save_message(self) -> None:
        """保存消息到数据库"""
        full_response_content = []
        full_response_reasoning_content = []
        # 保存AI响应到数据库
        if self.chat_request.llm_model == "deepseek-reasoner":
            async with self.db.begin():
                # 将空列表转换为 None
                reasoning_content = ''.join(
                    full_response_reasoning_content) if full_response_reasoning_content else None
                message_content = ''.join(full_response_content) if full_response_content else None
                ai_message = Message(
                    message_id=assistant_message_id,
                    message_role="assistant",
                    llm_model=self.chat_request.llm_model,
                    reasoning_content=reasoning_content,
                    message_content=message_content,
                    chat_id=self.chat_request.chat_id
                )
                self.db.add(ai_message)
                await self.db.commit()
        # 更新聊天记录时间戳
        async with self.db.begin():
            result = await self.db.execute(select(ChatHistory).where(ChatHistory.chat_id == self.chat_request.chat_id))
            chat_history_record = result.scalar_one_or_none()
            if chat_history_record:
                chat_history_record.timestamp = datetime.now(timezone.utc)
            else:
                raise ValueError("指定的 chat_id 不存在")
            await self.db.commit()
        pass

    async def generate(self):
        response_stream = await self.llm_client.chat.completions.create(
            # model="deepseek-chat",
            model=self.chat_request.llm_model,
            messages=messages,
            stream=True  # 流式模型
        )
        return response_stream

    async def chat_handle(self):
        pass
