# app/services/chat_service.py

import asyncio
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Session, Message
from agent.react_agent import ReactAgent


class ChatService:

    def __init__(self):
        self.agent = ReactAgent()

    # ------------------------
    # 创建会话
    # ------------------------
    async def create_session(
        self,
        db: AsyncSession,
        title: str | None = None,
        user_id: int = 0,
    ):
        try:
            final_title = title.strip() if isinstance(title, str) else ""
            if final_title.lower() == "new trip plan":
                final_title = ""
            if not final_title:
                final_title = f"session-{uuid.uuid4().hex[:6]}"
            session = Session(user_id=user_id, title=title)
            session.title = final_title
            db.add(session)
            await db.commit()
            await db.refresh(session)
            return session
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------------
    # 校验 session 是否存在
    # ------------------------
    async def session_exists(self, db: AsyncSession, session_id: int) -> bool:
        result = await db.execute(
            select(Session.id).where(Session.id == session_id)
        )
        return result.scalar_one_or_none() is not None

    # ------------------------
    # 获取历史（滑动窗口）
    # ------------------------
    async def get_messages(
        self,
        db: AsyncSession,
        session_id: int,
        limit: int = 20,
    ):
        result = await db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.id.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        return list(reversed(messages))

    # ------------------------
    # 保存消息
    # ------------------------
    async def save_message(
        self,
        db: AsyncSession,
        session_id: int,
        role: str,
        content: str,
        tool_name: str | None = None,
    ):
        try:
            msg = Message(
                session_id=session_id,
                role=role,
                content=content,
                tool_name=tool_name,
            )
            db.add(msg)
            await db.commit()
            await db.refresh(msg)
            return msg
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------------
    # 构建上下文 prompt
    # ------------------------
    def build_prompt(self, history: list[Message]) -> str:
        lines = []
        for msg in history:
            if msg.role == "user":
                lines.append(f"用户: {msg.content}")
            elif msg.role == "assistant":
                lines.append(f"助手: {msg.content}")
        return "\n".join(lines)

    # ------------------------
    # 核心聊天流式（最终稳定版）
    # ------------------------
    async def chat_stream(
        self,
        db: AsyncSession,
        session_id: int,
        user_input: str,
    ):
        # 1️⃣ 获取历史
        history = await self.get_messages(db, session_id)

        # 2️⃣ 保存用户消息
        await self.save_message(db, session_id, "user", user_input)

        assistant_full_text = ""

        # 3️⃣ 流式输出
        messages = []
        for msg in history:
            if msg.role in {"user", "assistant"}:
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": user_input})

        try:
            async for chunk in self.agent.execute_stream(messages):
                if not chunk:
                    continue
                assistant_full_text += chunk
                yield chunk
                await asyncio.sleep(0)
        except Exception as e:
            yield f"[ERROR]{str(e)}"
            return

        # 4️⃣ 保存 assistant 完整回复
        final_text = assistant_full_text.strip()
        if not final_text:
            final_text = "我可以回答这个问题，但我刚才没有成功生成内容。请你重试一次，我会直接回答。"
            yield final_text

        await self.save_message(
            db,
            session_id,
            "assistant",
            final_text,
        )

        yield "[DONE]"


    # ------------------------
    # 会话列表
    # ------------------------
    async def get_session_list(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
    ):
        offset = (page - 1) * page_size

        total_result = await db.execute(select(Session))
        total = len(total_result.scalars().all())

        result = await db.execute(
            select(Session)
            .order_by(Session.id.desc())
            .offset(offset)
            .limit(page_size)
        )
        sessions = result.scalars().all()

        return total, sessions

    # ------------------------
    # 消息列表
    # ------------------------
    async def get_message_list(
        self,
        db: AsyncSession,
        session_id: int,
        limit: int = 50,
    ):
        session_result = await db.execute(
            select(Session).where(Session.id == session_id)
        )
        session = session_result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        result = await db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.id.asc())
            .limit(limit)
        )
        messages = result.scalars().all()

        return messages
