from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ProfilePictureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    image: str
    created_at: datetime
    updated_at: datetime
