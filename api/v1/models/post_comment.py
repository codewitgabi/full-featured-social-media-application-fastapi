from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.v1.models.abstract_base import AbstractBaseModel
import api.v1.models as models


class PostComment(AbstractBaseModel):
    __tablename__ = "post_comment"

    post_id: Mapped[str] = mapped_column(ForeignKey("post.id"))
    post: Mapped["models.post.Post"] = relationship(back_populates="comments")
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __str__(self) -> str:
        return self.comment
