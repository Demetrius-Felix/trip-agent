from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback
import sys
import os

# 导入当前业务使用到的模型
from models import Session, Message



from app.api import chat

app = FastAPI(title="智能旅行规划系统")

# 添加 CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许的源
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"],    # 允许的请求方法
    allow_headers=["*"],    # 允许的请求头
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = f"Global Exception: {str(exc)}\n{traceback.format_exc()}"
    print(error_msg, file=sys.stderr)
    try:
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(error_msg + "\n" + "-"*50 + "\n")
    except Exception:
        pass
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )

@app.get("/ping")
async def ping():
    return {"message": "pong"}

# 挂载路由
app.include_router(chat.router)
