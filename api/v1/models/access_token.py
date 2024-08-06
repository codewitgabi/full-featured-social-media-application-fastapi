from datetime import datetime
from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from api.v1.models.abstract_base import AbstractBaseModel
import api


class AccessToken(AbstractBaseModel):
    __tablename__ = "access_token"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped["api.v1.models.user.User"] = relationship(
        back_populates="access_tokens"
    )
    token: Mapped[str] = mapped_column(String(500), nullable=False)
    expiry_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __str__(self) -> str:
        return self.token
