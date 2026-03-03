# models/sessions.py

from sqlalchemy import BigInteger, String, SmallInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="会话ID"
    )

    # 使用 Mapped 类型
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        index=True,
        comment="所属用户ID(可为空)"
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="会话标题"
    )

    status: Mapped[int] = mapped_column(
        SmallInteger,
        default=1,
        comment="会话状态 1=进行中 2=完成 0=删除"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="创建时间"
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )

    # 关联消息（级联删除）
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True
    )