from typing import List, Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    func,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.v1.models.abstract_base import AbstractBaseModel
from api.v1.utils.database import Base
import api


# role enum


class RoleEnum(Enum):
    user = "user"
    admin = "admin"


followers_table = Table(
    "user_interaction",
    Base.metadata,
    Column("follower_id", String, ForeignKey("user.id"), primary_key=True),
    Column("followed_id", String, ForeignKey("user.id"), primary_key=True),
)


class User(AbstractBaseModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(1024), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(1024))
    contact_into: Mapped[Optional[str]] = mapped_column(String(15))
    social_links: Mapped[List] = mapped_column(String(255), nullable=True)
    followers = relationship(
        "User",
        secondary=followers_table,
        primaryjoin=lambda: User.id == followers_table.c.followed_id,
        secondaryjoin=lambda: User.id == followers_table.c.follower_id,
    )
    role: Mapped[str] = mapped_column(SQLAlchemyEnum(RoleEnum), default=RoleEnum.user)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    cover_photos: Mapped[list["api.v1.models.cover_photo.CoverPhoto"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    posts: Mapped[List["api.v1.models.post.Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    access_tokens: Mapped[List["api.v1.models.access_token.AccessToken"]] = (
        relationship(back_populates="user", cascade="all, delete-orphan")
    )

    def __str__(self) -> str:
        return self.username
