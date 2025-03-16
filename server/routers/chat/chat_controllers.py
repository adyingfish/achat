# controllers.py
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

from openai import OpenAI, AsyncOpenAI

router = APIRouter()

# 创建会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
AsyncSessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

client = OpenAI(
    api_key="",
    base_url="https://api.deepseek.com"
)
async_client = AsyncOpenAI(
    api_key="",
    base_url="https://api.deepseek.com"
)


# 依赖项 - 获取数据库会话
def get_db():
    db = SessionLocal()  # 创建一个数据库会话
    try:
        yield db  # 提供数据库会话给调用它的函数
    finally:
        db.close()  # 在函数执行完毕后，关闭数据库绘会话


async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()


# 请求体模型

class ChatHistoryRequest(BaseModel):
    authed_user_id: str


class ChatHistoryRespose(BaseModel):
    chat_id: str
    label: str


# 定义请求体模型
class ChatRequest(BaseModel):
    message_id: str
    user_message: str
    chat_id: str
    llm_model: str


@router.post("/chat_stream")
async def chat_stream(
        request: Request,
        chat_request: ChatRequest,
        db: AsyncSession = Depends(get_async_db),
):
    try:
        client = AsyncOpenAI(
            api_key="",
            base_url="https://api.deepseek.com"
        )
        # chat_id = uuid.uuid4()
        full_response_content = []
        full_response_reasoning_content = []
        user_id = request.session.get("user").get("authed_user_id")
        user_uuid = request.session.get("user").get("authed_user_uuid")
        # 处理对话初始化
        async with db.begin():
            # 验证现有对话归属
            result = await db.execute(
                select(ChatHistory).where(
                    ChatHistory.chat_id == chat_request.chat_id,
                    ChatHistory.user_uuid == user_uuid,
                    ChatHistory.user_id == user_id,
                )
            )
            if not result.scalar():
                chat_history = ChatHistory(
                    chat_id=chat_request.chat_id,
                    chat_topic=chat_request.user_message[:32],
                    user_id=user_id,
                    user_uuid=user_uuid,
                )
                db.add(chat_history)

            # 保存用户消息
            user_message = Message(
                message_id=chat_request.message_id,
                # message_id=uuid.uuid4(),
                message_role="user",
                message_content=chat_request.user_message,
                chat_id=chat_request.chat_id
            )
            db.add(user_message)
            await db.commit()

        # 构建完整对话上下文
        messages = await build_chat_context(db, chat_request.chat_id)

        # 创建流式响应
        response_stream = await client.chat.completions.create(
            # model="deepseek-chat",
            model=chat_request.llm_model,
            messages=messages,
            stream=True  # 流式模型
        )

        assistant_message_id = uuid.uuid4()

        async def generate():

            # 首先发送消息ID
            yield f"data: {json.dumps({'assistant_message_id': str(assistant_message_id)}, ensure_ascii=False)}\n\n"

            async for chunk in response_stream:
                if chat_request.llm_model == "deepseek-reasoner":
                    if chunk.choices[0].delta.reasoning_content:
                        reasoning_content = chunk.choices[0].delta.reasoning_content or ""
                        full_response_reasoning_content.append(reasoning_content)
                        yield f"data: {json.dumps({'reasoning_content': reasoning_content}, ensure_ascii=False)}\n\n"
                    else:
                        content = chunk.choices[0].delta.content or ""
                        full_response_content.append(content)
                        yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"
                else:
                    content = chunk.choices[0].delta.content or ""
                    full_response_content.append(content)
                    yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"
            # 保存AI响应到数据库
            if chat_request.llm_model == "deepseek-reasoner":
                async with db.begin():
                    ai_message = Message(
                        message_id=assistant_message_id,
                        message_role="assistant",
                        llm_model=chat_request.llm_model,
                        reasoning_content=''.join(full_response_reasoning_content),
                        message_content=''.join(full_response_content),
                        chat_id=chat_request.chat_id
                    )
                    db.add(ai_message)
                    await db.commit()
            else:
                async with db.begin():
                    ai_message = Message(
                        message_id=assistant_message_id,
                        message_role="assistant",
                        llm_model=chat_request.llm_model,
                        message_content=''.join(full_response_content),
                        chat_id=chat_request.chat_id
                    )
                    db.add(ai_message)
                    await db.commit()
            # 更新聊天记录时间戳
            async with db.begin():
                result = await db.execute(select(ChatHistory).where(ChatHistory.chat_id == chat_request.chat_id))
                chat_history_record = result.scalar_one_or_none()
                if chat_history_record:
                    chat_history_record.timestamp = datetime.now(timezone.utc)
                else:
                    raise ValueError("指定的 chat_id 不存在")
                await db.commit()

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def build_chat_context(db: AsyncSession, chat_id: UUID) -> List[Dict]:
    """构建符合模型要求的对话上下文"""
    result = await db.execute(
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

    # # 确保以user消息结尾（当前消息已包含）
    # if context and context[-1]["role"] != "user":
    #     context = context[:-1]  # 移除最后的assistant消息

    return context


@router.post("/chat", response_model=dict)
async def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": request.user_message}
            ],
            stream=False
        )
        # 返回模型生成的回答
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 定义获取聊天记录的接口，依赖于当前用户的认证
@router.get("/chat_history_list_get", response_model=List[Dict])
async def get_chat_history_list(request: Request, db: Session = Depends(get_db)):
    try:
        print(request.session.get("user"))
        # 通过 SQLAlchemy ORM 查询当前用户的历史聊天记录
        chat_history_list = (
            db.query(ChatHistory)
            .filter(ChatHistory.user_id == request.session.get("user").get("authed_user_id"))
            .order_by(ChatHistory.timestamp.desc())
            .all()
        )

        # 可选择将 ORM 对象转换为字典格式返回
        chat_history = [
            {
                "chat_id": chat.chat_id,
                "chat_topic": chat.chat_topic,
                # "timestamp": chat.timestamp
            }
            for chat in chat_history_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return chat_history


# 定义获取聊天记录的接口
@router.get("/chat_history_id_get/", response_model=List[Dict])
async def get_chat_history_id(chat_id: uuid.UUID = Query(..., description="Chat ID"), db: Session = Depends(get_db)):
    try:
        # 通过 SQLAlchemy ORM 查询当前用户的历史聊天记录
        message_list = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.timestamp)
            .all()
        )
        # 可选择将 ORM 对象转换为字典格式返回
        message_list = [
            {
                "message_id": message.message_id,
                "message_role": message.message_role,
                "reasoning_content": message.reasoning_content,
                "message_content": message.message_content,
                # "message": chat.message,
                # "timestamp": chat.timestamp
            }
            for message in message_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return message_list
