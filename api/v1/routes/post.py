from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.v1.models.user import User
from api.v1.responses.success_response import success_response
from api.v1.schemas.post import CreatePostSchema, UpdatePostSchema
from api.v1.utils.dependencies import get_db
from api.v1.services.user import user_service
from api.v1.services.post import post_service


posts = APIRouter(prefix="/posts", tags=["post"])


@posts.post("")
async def create_post(
    post: CreatePostSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):
    new_post = post_service.create(db=db, user=user, schema=post)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Post created successfully",
        data=new_post,
    )


@posts.delete(
    "/{id}",
    summary="Delete a post",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    id: str,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):
    post_service.delete(db=db, user=user, post_id=id)

    return success_response(
        status_code=status.HTTP_204_NO_CONTENT, message="Post deleted successfully"
    )


@posts.patch("/{id}", summary="Update a post", status_code=status.HTTP_200_OK)
async def update_post(
    id: str,
    schema: UpdatePostSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):
    updated_post = post_service.update(db=db, user=user, post_id=id, schema=schema)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Post updated successfully",
        data=updated_post,
    )
