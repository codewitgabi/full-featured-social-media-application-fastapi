from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.v1.schemas.post_comment import UpdateCommentSchema, CreateCommentSchema
from api.v1.services.post_comment import comment_service
from api.v1.utils.dependencies import get_db
from api.v1.services.user import user_service
from api.v1.services.post import post_service
from api.v1.models.user import User
from api.v1.models.post import Post

comments = APIRouter(prefix="/comments", tags=["comment"])

@comments.post("/{post_id}")
async def create_comment(
        post_id:str,
        comment: CreateCommentSchema,
        db: Session = Depends(get_db),
        user: User = Depends(user_service.get_current_user)):

    new_comment = comment_service.create(db=db, user=user, post_id=post_id, schema=comment)

    return success_response(
            status_code=status.HTTP_201_CREATED,
            message="Comment successfully created",
            data=new_comment)

