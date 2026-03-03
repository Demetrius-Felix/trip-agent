from datetime import datetime
from typing import List

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DateTime,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

class User(Base):
    """
    用户基础信息表
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="用户ID"
    )

    nickname: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="用户昵称"
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        comment="用户邮箱"
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="头像URL"
    )

    status: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="用户状态 1=正常 0=禁用"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        comment="创建时间"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新时间"
    )

    # 关系
    sessions: Mapped[List["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    preferences: Mapped[List["UserPreference"]] = relationship(
        "UserPreference",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, nickname={self.nickname})>"

class UserPreference(Base):
    """
    用户长期偏好信息表
    """
    __tablename__ = "user_preferences"

    __table_args__ = (
        UniqueConstraint("user_id", "preference_key", name="uniq_user_pref"),
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="用户ID"
    )
    
    preference_key: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    preference_value: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="preferences")
