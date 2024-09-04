from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.v1.schemas.post_comment import CreateCommentSchema, CommentResponse
from api.v1.services.post_comment import comment_service
from api.v1.utils.dependencies import get_db
from api.v1.services.user import user_service
from api.v1.services.post import post_service
from api.v1.models.user import User
from api.v1.models.post import Post
from api.v1.responses.success_response import success_response


comments = APIRouter(prefix="/posts", tags=["comment"])


@comments.post("/{post_id}/comments")
async def create_comment(
    post_id: str,
    comment: CreateCommentSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):

    new_comment: CommentResponse = comment_service.create(
        db=db, user=user, post_id=post_id, schema=comment
    )

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Comment successfully created",
        data=new_comment,
    )


@comments.patch("/{post_id}/comments/{comment_id}")
async def update_comment(
    post_id: str,
    comment_id: str,
    comment: CreateCommentSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):

    updated_comment = comment_service.update(
        db=db, user=user, post_id=post_id, comment_id=comment_id, schema=comment
    )

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Comment updated successfully",
        data=updated_comment,
    )


@comments.delete("/{post_id}/comments/{comment_id}")
async def delete_comment(
    post_id: str,
    comment_id: str,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):

    comment_service.delete(db=db, user=user, post_id=post_id, comment_id=comment_id)

    return success_response(
        status_code=status.HTTP_204_NO_CONTENT, message="Comment deleted successfully"
    )
