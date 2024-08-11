from datetime import datetime
from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, ForeignKey, String, func
from api.v1.models.abstract_base import AbstractBaseModel


class Post(AbstractBaseModel):
    __tablename__ = "post"

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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __str__(self) -> str:
        return self.content or self.image or self.video
