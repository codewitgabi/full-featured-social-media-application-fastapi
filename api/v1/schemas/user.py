from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, root_validator
from api.v1.schemas.profile_picture import ProfilePictureResponse


class UserBase(BaseModel):
    username: str = Field(max_length=255)
    email: EmailStr
    role: Literal["user", "admin"] = "user"


class UserCreate(UserBase):
    password: str


class UserCreateResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    access_token: str
    expiry: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Used for comment to provide extra details about user
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    profile_pictures: List[ProfilePictureResponse] = Field(default=None, exclude=True)
    current_profile_picture: Optional[ProfilePictureResponse] = Field(
        default=None, serialization_alias="profile_picture"
    )

    @root_validator(pre=True)
    def set_current_profile_picture(cls, values):
        profile_pictures = values.get("profile_pictures", [])
        if profile_pictures:
            latest_profile_picture = max(
                profile_pictures, key=lambda picture: picture["updated_at"]
            )
            values["current_profile_picture"] = latest_profile_picture
        return values


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
