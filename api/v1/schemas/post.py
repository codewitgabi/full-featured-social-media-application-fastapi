from pydantic import BaseModel, ConfigDict, UUID4
from api.v1.schemas.user import UserResponse

class CreatePostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str | None = None
    image: str | None = None
    video: str | None = None


class UpdatePostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str | None = None
    image: str | None = None
    video: str | None = None


class LikeResponse(BaseModel):
    model_config = ConfigDict(from_attribute=True)

    id: UUID4
    post_id: UUID4
    user_id: UUID4
    liked: bool
    user: UserResponse = None
