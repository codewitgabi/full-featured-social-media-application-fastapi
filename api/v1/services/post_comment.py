from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.v1.schemas.post_comment import CreateCommentSchema, UpdateCommentSchema, CommentResponse
from api.v1.models.post_comment import PostComment
from api.v1.models.post import Post
from api.v1.models.user import User


class CommentService:
    # class attributes
    post_not_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post does not exist")

    comment_not_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Comment does not exist")
    # end of class attributes

    # class methods
    def create(self, db: Session, user: User, post_id:str, schema: CreateCommentSchema):
        schema_dict = schema.model_dump()

        if all(value is None for value in schema_dict.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The comment cannot be an empty field")
        
        # get the post
        post = db.query(Post).filter(Post.user_id == user.id, Post.id==post_id).first()

        if not post:
            raise self.post_not_found

        comment = PostComment(user_id = user.id, post_id = post.id, **schema_dict)

        response_user = jsonable_encoder(user)

        db.add(comment)
        db.commit()
        db.refresh(comment)

        encoded = jsonable_encoder(comment)
        encoded["user"] = response_user
        del encoded["user_id"]

        return CommentResponse(**encoded)


    def get_comments(self, db: Session, user: User, post_id: str):
        post = db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()

        if not post:
            raise self.post_not_found

        comments = db.query(PostComment).filter(PostComment.post_id == post_id).all()

        if not comment:
            raise self.comment_not_found

        return jsonable_encoder(comments)


    def delete(self, db:Session, user: User, post_id: str, comment_id: str):

        post = db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()

        if not post:
            raise self.post_not_found

        comment = db.query(PostComment).filter(
                PostComment.id == comment_id, 
                PostComment.post_id == post.id, 
                PostComment.user_id == user.id
                ).first()

        if not comment:
            raise self.comment_not_found

        db.delete(comment)
        db.commit()


    def update(self, db: Session, user: User, post_id: str, comment_id: str, schema: UpdateCommentSchema):

        schema_dict = schema.model_dump()

        if schema_dict.comment is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The comment cannot be an empty field")

        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise self.post_not_found

        comment = db.query(PostComment).filter(
                PostComment.post_id == post.id, 
                PostComment.id == comment_id,
                PostComment.user_id == user.id
                ).first()

        if not comment:
            raise self.comment_not_found

        for attr, value in schema_dict.items():
            if value:
                setattr(comment, attr, value)

        db.commit()
        db.refresh(comment)

        return jsonable_encoder(comment)

    # end of class methods

comment_service = CommentService()
