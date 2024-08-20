from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from api.v1.models.abstract_base import AbstractBaseModel


class SocialLink(AbstractBaseModel):
    __tablename__ = "social_link"

    link: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="social_links")

    def __str__(self) -> str:
        return self.link
