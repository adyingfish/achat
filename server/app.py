# app.py Starlette for the web parts.& Pydantic for the data parts
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 导入CORS中间件
from starlette.middleware.sessions import SessionMiddleware
from routers import controllers, llm
from routers.user import user_controllers
from routers.chat import chat_controllers

# from routers import controllers, llm_test

app = FastAPI(
    title="LLM Server",
    version="1.0",
    description="A simple llm ai chat web application server api",
)

# 添加 Session 中间件（确保在 CORS 之前）
app.add_middleware(
    SessionMiddleware,
    secret_key="test_secret_key",
    # https_only=False,  # 允许 HTTP 发送 Cookie
    # same_site="Lax",
)

# 配置跨域规则，启用CORS，允许任何来源访问以 /api/ 开头的接口
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],  # 可以指定特定的域名，例如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有的HTTP方法
    allow_headers=["*"],  # 允许所有的HTTP头
)

app.include_router(user_controllers.router, prefix="/api/v1/user", tags=["user"])
app.include_router(chat_controllers.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["llm"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
