from datetime import datetime
from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, ForeignKey, String, func
from api.v1.models.abstract_base import AbstractBaseModel
from pydantic import UUID4
from sqlalchemy.orm import remote
from uuid import uuid4


class Post(AbstractBaseModel):
    __tablename__ = "post"

    post_id: Mapped[str] = mapped_column(unique=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")
    content: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(
        String(1024), nullable=True
    )  # image url
    video: Mapped[Optional[str]] = mapped_column(
        String(1024), nullable=True
    )  # video url
    comments = relationship("PostComment", back_populates="post")
    original_post_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("post.id"), nullable=True
    )
    original_post = relationship(
        "Post",
        primaryjoin=lambda: Post.original_post_id == remote(Post.id),
        backref="reposts",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __str__(self) -> str:
        return self.content or self.image or self.video


class Like(AbstractBaseModel):
    __tablename__ = "like"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", backref="my_likes")
    post_id: Mapped[str] = mapped_column(ForeignKey("post.id"))
    post = relationship("Post", backref="likes")
    liked: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return self.user
