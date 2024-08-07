from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from api.v1.models.abstract_base import AbstractBaseModel


class AccessToken(AbstractBaseModel):
    __tablename__ = "access_token"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="access_tokens")
    token: Mapped[str] = mapped_column(String(500), nullable=False)
    expiry_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    blacklisted: Mapped[bool] = mapped_column(
        Boolean(), server_default="false", default=False
    )

    def __str__(self) -> str:
        return self.token
