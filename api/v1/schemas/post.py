from pydantic import BaseModel, ConfigDict


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


class PostResponse(BaseModel):
    pass
