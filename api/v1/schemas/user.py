from typing import Literal
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(max_length=255)
    email: EmailStr
    role: Literal["user", "admin"] = "user"


class UserCreate(UserBase):
    password: str


class UserCreateResponse(BaseModel):
    id: str
    username: str
    email: str
    access_token: str
