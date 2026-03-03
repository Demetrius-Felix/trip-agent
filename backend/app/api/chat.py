# app/api/chat.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.chat_service import ChatService
from core.database import get_db

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()


# -----------------------
# 创建会话
# -----------------------
@router.post("/session")
async def create_session(
    title: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    session = await chat_service.create_session(db, title)
    return {
        "session_id": session.id,
        "title": session.title,
    }


# -----------------------
# 流式聊天
# -----------------------
@router.get("/stream/{session_id}")
async def chat_stream(
    session_id: int,
    query: str,
    db: AsyncSession = Depends(get_db),
):
    # 校验 session 是否存在
    exists = await chat_service.session_exists(db, session_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Session not found")

    def format_sse(data: str) -> str:
        text = str(data)
        lines = text.split("\n")
        return "".join([f"data: {line}\n" for line in lines]) + "\n"

    async def event_generator():
        yield ": connected\n\n"
        try:
            async for chunk in chat_service.chat_stream(
                    db,
                    session_id,
                    query,
            ):
                yield format_sse(chunk)
        except Exception as e:
            yield format_sse(f"[ERROR]{str(e)}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

# -----------------------
# 会话列表
# -----------------------
@router.get("/session/list")
async def get_session_list(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    total, sessions = await chat_service.get_session_list(
        db,
        page,
        page_size,
    )

    return {
        "total": total,
        "items": [
            {
                "session_id": s.id,
                "title": s.title,
                "created_at": s.created_at,
            }
            for s in sessions
        ],
    }


# -----------------------
# 消息列表
# -----------------------
@router.get("/message/list/{session_id}")
async def get_message_list(
    session_id: int,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    messages = await chat_service.get_message_list(
        db,
        session_id,
        limit,
    )

    return {
        "session_id": session_id,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at,
            }
            for m in messages
        ],
    }
