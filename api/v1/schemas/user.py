from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, Field, EmailStr

from api.v1.models.user import User


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
    expiry: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    bio: str | None
    contact_info: str | None
    social_links: List[str] | None = None
    role: str
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    expiry: datetime
    user: UserLoginSchema

    class Config:
        from_attributes = True
