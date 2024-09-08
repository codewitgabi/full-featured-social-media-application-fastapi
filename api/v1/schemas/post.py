from pydantic import BaseModel, ConfigDict, UUID4, Field
from api.v1.schemas.user import UserResponse
from datetime import datetime
from typing import Optional


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


class PostResponse(CreatePostSchema):

    id: UUID4
    user_id: UUID4 = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    user: UserResponse | None = Field(default=None, serialization_alias="original_post_owner")


class PostResponseSchema(PostResponse):
    original_post: PostResponse | None = Field(default=None, serialization_alias="original_post")


class LikeResponse(BaseModel):
    model_config = ConfigDict(from_attribute=True)

    id: str
    post_id: str
    user_id: str
    liked: bool
    user: UserResponse = None


class RepostCreate(BaseModel):

    content: str | None = None


class RepostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    post_id: str = Field(exclude=True)
    user_id: str = Field(exclude=True)
    content: str | None = None
    created_at: datetime
    updated_at: datetime
    user: UserResponse = Field(default=None, serialization_alias="post_owner")
    post: PostResponse = Field(default=None, serialization_alias="original_post")
