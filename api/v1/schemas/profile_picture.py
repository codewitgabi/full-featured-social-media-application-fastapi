from pydantic import BaseModel, ConfigDict


class ProfilePictureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    image: str
