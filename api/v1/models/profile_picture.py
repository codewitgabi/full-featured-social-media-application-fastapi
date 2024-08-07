from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, ForeignKey, String, func
from api.v1.models.abstract_base import AbstractBaseModel
import api


class ProfilePicture(AbstractBaseModel):
    __tablename__ = "profile_picture"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    image: Mapped[str] = mapped_column(String(1024), nullable=False)
    user: Mapped["api.v1.models.user.User"] = relationship(
        back_populates="profile_pictures"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __str__(self) -> str:
        return self.image
