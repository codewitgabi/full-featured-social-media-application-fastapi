from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .user import UserResponse

class CreateCommentSchema(BaseModel):
     model_config = ConfigDict(from_attributes=True)

     comment: str | None = None


class UpdateCommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    comment: str | None = None


class CommentResponse(BaseModel):
    id: str
    comment: str
    created_at: datetime
    updated_at: datetime
    post_id: str
    user: UserResponse
