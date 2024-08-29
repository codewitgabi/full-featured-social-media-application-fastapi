from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CreateCommentSchema(BaseModel):
     model_config = ConfigDict(from_attributes=True)

     comment: str


class UpdateCommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    comment: str
