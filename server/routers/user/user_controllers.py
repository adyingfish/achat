# controllers.py
import uuid

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from routers.models.models import engine, sync_engine, User, ChatHistory, Message
from typing import List

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
# 用户注册
class UserSignUp(BaseModel):
    user_id: str
    password: str


# 用户登录
class UserSignIn(BaseModel):
    user_id: str
    password: str


# 用户注册
@router.post("/signup", response_model=dict)
async def user_sign_up(user: UserSignUp, db: AsyncSession = Depends(get_async_db)):
    # 检查userid是否已存在
    result = await db.execute(select(User).filter(User.user_id == user.user_id))
    existing_user = result.scalars().first()
    if existing_user:
        return {"status": "False", "message": "User with this user_id already exists"}
    user_uuid = uuid.uuid4()  # 生成唯一的用户UUID
    new_user = User(
        user_uuid=user_uuid,  # 存储生成的UUID
        user_id=user.user_id,
        password=user.password,
        username=user.user_id,
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"status": "True", "message": "Sign Up successful"}

    except SQLAlchemyError as e:
        await db.rollback()
        return {"status": "Error", "message": f"Database error: {str(e)}"}


# 用户登录
@router.post("/signin", response_model=dict)
async def user_sign_in(user: UserSignIn, request: Request, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(select(User).filter(User.user_id == user.user_id))
        existing_user = result.scalars().first()
        if not existing_user:
            return {"status": "False", "message": "User not found"}
        # 验证密码
        if existing_user.password != user.password:
            return {"status": "False", "message": "Incorrect password"}
        # 记录用户 Session（关键步骤）
        request.session["user"] = {
            "authed_user_id": existing_user.user_id,
            "authed_user_uuid": str(existing_user.user_uuid)
        }
        return {"status": "True", "message": "Login successful"}

    except SQLAlchemyError as e:
        return {"status": "Error", "message": f"Database error: {str(e)}"}


# 获取当前用户信息
@router.get("/me", response_model=dict)
async def uesr_get_current(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not signed in")
    return {"status": "True", "user": user}


# 退出登录
@router.post("/signout", response_model=dict)
async def user_sign_out(request: Request):
    request.session.clear()  # 清除 session
    return {"status": "True", "message": "Signed out"}
