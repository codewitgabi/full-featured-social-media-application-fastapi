from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


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


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    contact_info: Optional[str] = None
    social_links: Optional[List[str]] = None
    profile_picture: Optional[str] = None
    cover_photo: Optional[str] = None


class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    expiry: datetime
    user: UserLoginSchema
