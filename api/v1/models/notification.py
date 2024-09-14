from enum import Enum
from sqlalchemy import String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from api.v1.models.abstract_base import AbstractBaseModel


class NotificationStatus(Enum):
    read = "read"
    unread = "unread"


class Notification(AbstractBaseModel):
    __tablename__ = "notification"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    message: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        SQLAlchemyEnum(NotificationStatus), server_default="unread"
    )

    user = relationship("User", back_populates="notifications")

    def __str__(self):
        return self.message
