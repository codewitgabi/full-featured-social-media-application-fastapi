from typing import Annotated
from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
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


@users.patch("/{followee_id}/follow", summary="Follow a particular user")
async def follow(
    followee_id: str,
    background_task: BackgroundTasks = BackgroundTasks(),
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):

    user_service.follow_user(db=db, user=user, user_id=followee_id, background_task=background_task)

    return success_response(
        status_code=200,
        message="User followed successfully",
    )


@users.delete("/{followee_id}/unfollow", summary="Unfollow the user with the id")
async def unfollow(
    followee_id: str,
    background_task: BackgroundTasks = BackgroundTasks(),
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):

    user_service.unfollow_user(db=db, user_id=followee_id, user=user, background_task=background_task)

    return success_response(
        status_code=200,
        message="User unfollowed successfully",
    )


@users.get("/{user_id}/followers", summary="List of folllowers")
async def followers(
    user_id: str,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):

    followers = user_service.followers(db=db, user=user)

    return success_response(
        status_code=200, message="Followers successfully returned", data=followers
    )


@users.get(
    "/{user_id}/followings", summary="List of user the current user is following"
)
async def followings(
    user_id: str,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):

    followings = user_service.followings(db=db, user=user)

    return success_response(
        status_code=200,
        message="Followings list successfully returned",
        data=followings,
    )
