from fastapi import HTTPException, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.v1.schemas.post_comment import (
    CreateCommentSchema,
    CommentResponse,
    UpdateCommentSchema,
)
from api.v1.schemas.user import UserResponse
from api.v1.models.post_comment import PostComment
from api.v1.models.post import Post
from api.v1.models.user import User
from api.v1.models.notification import Notification
from api.v1.services.user import user_service
from api.v1.services.notification import notification_service


class CommentService:
    # class attributes
    post_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist"
    )

    comment_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist"
    )

    # end of class attributes

    # class methods
    def create(
            self, db: Session, user: User, post_id: str, schema: CreateCommentSchema, background_task: BackgroundTasks
    ):
        schema_dict = schema.model_dump()

        if all(value is None for value in schema_dict.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The comment cannot be an empty field",
            )

        # get the post
        post = (
            db.query(Post).filter(Post.id == post_id).first()
        )

        if not post:
            raise self.post_not_found

        comment = PostComment(user_id=user.id, post_id=post.id, **schema_dict)

        # get user complete details and serialize the user
        comment_owner = user_service.get_user_detail(db=db, user_id=user.id)
        response_user = jsonable_encoder(comment_owner)

        db.add(comment)
        db.commit()
        db.refresh(comment)

        encoded = jsonable_encoder(comment)
        encoded["user"] = response_user

        # Comment Notification
        notification = Notification(user_id=post.user_id, message=f"{user.username} commented on your post")

        db.add(notification)
        db.commit()

        # add background task to send notifcation
        background_task.add_task(notification_service.user_event_queues[notification.user_id].put, notification.message)


        return CommentResponse(**encoded)

    def update(
        self,
        db: Session,
        user: User,
        post_id: str,
        comment_id: str,
        schema: UpdateCommentSchema,
    ):

        schema_dict = schema.model_dump()

        if all(value is None for value in schema_dict.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The comment cannot be an empty field",
            )
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise self.post_not_found

        comment = (
            db.query(PostComment)
            .filter(
                PostComment.post_id == post.id,
                PostComment.id == comment_id,
                PostComment.user_id == user.id,
            )
            .first()
        )
        if not comment:
            raise self.comment_not_found

        for attr, value in schema_dict.items():
            if value:
                setattr(comment, attr, value)

        comment_owner = user_service.get_user_detail(db=db, user_id=user.id)
        response_user = jsonable_encoder(comment_owner)

        db.commit()
        db.refresh(comment)

        encoded = jsonable_encoder(comment)
        encoded["user"] = response_user

        return CommentResponse(**encoded)

    def delete(self, db: Session, user: User, post_id: str, comment_id: str):

        post = (
            db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()
        )

        if not post:
            raise self.post_not_found

        comment = (
            db.query(PostComment)
            .filter(
                PostComment.id == comment_id,
                PostComment.post_id == post.id,
                PostComment.user_id == user.id,
            )
            .first()
        )

        if not comment:
            raise self.comment_not_found

        db.delete(comment)
        db.commit()




    def get_comments(self, db: Session, user: User, post_id: str
):

        post = db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()

        if not post:
            raise self.post_not_found

        comments = db.query(PostComment).filter(PostComment.post_id == post_id).all()

        response_comments = []

        for comment in comments:
            owner_details = user_service.get_user_detail(db=db, user_id=comment.user_id)
            response_user = jsonable_encoder(owner_details)
            validate_user = UserResponse(**response_user)
            response_comment = jsonable_encoder(comment)

            response_comment["user"] = validate_user.model_dump()

            response_comments.append(response_comment)


        return jsonable_encoder(response_comments)

    # end of class methods


comment_service = CommentService()
