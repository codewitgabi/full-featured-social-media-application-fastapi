from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.v1.models.user import User
from api.v1.responses.success_response import success_response
from api.v1.schemas.user import UserUpdateSchema
from api.v1.services.user import user_service
from api.v1.utils.dependencies import get_db


users = APIRouter(prefix="/users", tags=["user"])


@users.patch("/{id}", summary="Update user profile")
async def update_user_profile(
    id: str,
    body: UserUpdateSchema,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):
    data = user_service.update_user_profile(db=db, user=user, user_id=id, schema=body)

    return success_response(message="User profile updated successfully", data=data)


@users.get("/{id}", summary="Get user profile detail")
async def get_user_profile(
    id: str,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):
    data = user_service.get_user_detail(db=db, user_id=id)

    return success_response(
        message="User detail fetched successfully",
        data=jsonable_encoder(data, exclude=["password"]),
    )


@users.delete(
    "/{id}",
    summary="Delete user profile/account",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_profile(
    id: str,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):
    user_service.delete_user_profile(db=db, user=user, user_id=id)

    return success_response(status_code=204, message="User deleted successfully")


@users.get("", summary="Get list of users")
async def get_users(search: str = "", db: Session = Depends(get_db)):
    users = user_service.fetch_all(db=db, search=search)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User list fetched successfully",
        data=users,
    )
