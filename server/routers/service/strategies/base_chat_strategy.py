from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID

from openai import AsyncOpenAI
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from routers.models.models import Message, ChatHistory


class ChatRequest(BaseModel):
    message_id: str
    user_message: str
    chat_id: str
    llm_model: str
    chat_type: str


# class ChatStrategy:
#     async def execute(self, request: ChatRequest) -> ChatResult:
#         raise NotImplementedError

@dataclass
class BaseChatStrategy(ABC):
    """
    策略基类，定义所有工作流必须实现的方法
    """
    db: AsyncSession
    request: Request
    chat_request: ChatRequest
    llm_client: AsyncOpenAI = AsyncOpenAI(
            api_key="",
            base_url="https://api.deepseek.com"
        )

    @abstractmethod
    async def chat_init(self):
        """对话初始化以及基本基础操作"""
        return

    @abstractmethod
    async def build_chat_context(self) -> List[Dict]:
        """构建对话上下文"""
        pass

    @abstractmethod
    async def save_message(self) -> None:
        """保存消息到数据库"""
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

    @abstractmethod
    async def generate(self):
        pass

    @abstractmethod
    async def chat_handle(self):
        pass
