from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router


app = FastAPI(title="智能旅行规划系统")

# 添加 CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许的源
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"],    # 允许的请求方法
    allow_headers=["*"],    # 允许的请求头
)

# 挂载路由
app.include_router(chat_router)
