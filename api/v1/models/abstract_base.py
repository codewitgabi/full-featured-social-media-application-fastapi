from uuid import uuid4
from datetime import datetime
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from api.v1.utils.database import Base


class AbstractBaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=lambda: str(uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
