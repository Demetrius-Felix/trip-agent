# models/message.py

from sqlalchemy import (
    BigInteger,
    Text,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="消息ID"
    )

    session_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("sessions.id", ondelete="CASCADE"),
        index=True,
        comment="所属会话ID"
    )

    role: Mapped[str] = mapped_column(
        Enum("system", "user", "assistant", "tool", name="role_enum"),
        nullable=False,
        index=True,
        comment="消息角色类型"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="消息正文内容"
    )

    token_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="消息token数量"
    )

    tool_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="调用的工具名称"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="创建时间"
    )

    # 关联会话
    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="messages"
    )