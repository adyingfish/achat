# models.py
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, create_engine, JSON
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID

# PostgreSQL 连接配置
DATABASE_URL = ""
DATABASE_URL_ASYNC = ""

# 创建数据库引擎
engine = create_engine(DATABASE_URL)
sync_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)

# 创建基础类
Base = declarative_base()


# model 定义数据模型
class User(Base):
    __tablename__ = "user"

    user_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, unique=True)
    user_id = Column(String(32), index=True, nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    username = Column(String(64), nullable=False)
    profile_picture = Column(String(2048))
    phone_number = Column(String(24), index=True, unique=True)
    email = Column(String(255), index=True, unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))  # 可选的创建时间字段
    user_type = Column(String(16), default="User")  # 用户类型
    user_status = Column(String(16), default="not_active")  # 用户的可用状态，默认为True（表示可用）
    # 定义一对多、多对一、多对多关系，user有多个chathistorys
    chathistorys = relationship("ChatHistory", back_populates="user")


class ChatHistory(Base):
    __tablename__ = "chathistory"
    chat_id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, unique=True)
    # chat_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, unique=True)
    chat_topic = Column(String(32), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    # 外键
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.user_uuid"), index=True, nullable=False)
    user_id = Column(String(32), index=True, nullable=False)
    # 定义一对多、多对一、多对多关系
    user = relationship("User", back_populates="chathistorys")
    messages = relationship("Message", back_populates="chathistory")


class Message(Base):
    __tablename__ = "message"
    message_id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, unique=True)
    # message_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, unique=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))  # 自动添加当前时间戳
    message_role = Column(String(16), nullable=False)
    llm_model = Column(String(64))
    web_search_results = Column(JSON)
    reasoning_content = Column(Text)
    message_content = Column(Text)
    # 外键
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chathistory.chat_id"), index=True)

    # 定义一对多、多对一、多对多关系
    chathistory = relationship("ChatHistory", back_populates="messages")


if __name__ == "__main__":
    # 初始化，在数据库创建表
    Base.metadata.create_all(bind=engine)
