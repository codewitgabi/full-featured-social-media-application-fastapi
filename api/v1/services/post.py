from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
from api.v1.models.post import Post, Like
from api.v1.models.user import User
from api.v1.schemas.post import (
    CreatePostSchema,
    UpdatePostSchema,
    LikeResponse,
    RepostResponse,
    RepostCreate,
    PostResponse,
    PostResponseSchema
)
from api.v1.schemas.user import UserResponse
from api.v1.services.user import user_service


class PostService:
    def get_post(self, db: Session, user: User, post_id: str):
        post = db.query(Post).options(
                joinedload(Post.original_post),
                joinedload(Post.user)
                ).filter(Post.id == post_id).first()


        response_post = jsonable_encoder(post)
        return PostResponseSchema(**response_post)


    def get_feeds(self, db: Session, user: User):
        posts = db.query(Post).all()

        posts_response = []
        for post in posts:
            
            detailed_post = self.get_post(db=db, user=user, post_id=post.id)
            posts_response.append(detailed_post)

        return posts_response


    def create(self, db: Session, user: User, schema: CreatePostSchema):
        schema_dict = schema.model_dump()

        if all(value is None for value in schema_dict.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide one of content, image or video",
            )

        post = Post(user_id=user.id, **schema_dict)

        db.add(post)
        db.commit()
        db.refresh(post)

        return jsonable_encoder(post)


    def delete(self, db: Session, user: User, post_id: str):
        # get post matching post_id and user

        post = (
            db.query(Post).filter(Post.user_id == user.id, Post.id == post_id).first()
        )

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        db.delete(post)
        db.commit()


    def update(self, db: Session, user: User, post_id: str, schema: UpdatePostSchema):
        # get post from db

        post = (
            db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
        )

        schema_dict = schema.model_dump()

        if all(value is None for value in schema_dict.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide one of content, image or video",
            )

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        for attr, value in schema_dict.items():
            if value:
                setattr(post, attr, value)

        db.commit()
        db.refresh(post)

        return jsonable_encoder(post)


    def like_post(self, db: Session, user: User, post_id: str):

        # get the post
        post = (
            db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
        )

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, details="Page not found"
            )

        # Check if user has already liked the post
        like = (
            db.query(Like)
            .filter(Like.post_id == post_id, Like.user_id == user.id)
            .first()
        )

        if like:
            db.delete(like)
            db.commit()
        else:
            like = Like(user_id=user.id, post_id=post_id)
            like.liked = True
            db.add(like)
            db.commit()


    def get_likes(self, db: Session, post_id: str, user: User):

        post = (
            db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
        )

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, details="Page not found"
            )

        likes = db.query(Like).filter(Like.post_id == post_id).all()

        likes_response = []

        for like in likes:

            owner_details = user_service.get_user_detail(db=db, user_id=like.user_id)
            response_user = jsonable_encoder(owner_details)
            validate_user = UserResponse(**response_user)

            like_response = jsonable_encoder(like)

            like_response["user"] = validate_user.model_dump()

            likes_response.append(like_response)

        return likes_response


    def repost(self, db: Session, post_id: str, user: User, schema: RepostCreate):

        original_post = db.query(Post).filter(Post.id == post_id).first()

        if not original_post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Ceeate new post
        new_post = Post(
            content=schema.content,
            user_id=user.id,
            original_post_id=post_id,
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        original_post_owner = user_service.get_user_detail(
            db=db, user_id=original_post.user_id
        )
        print(original_post_owner)

        new_post_owner = user_service.get_user_detail(db=db, user_id=user.id)
        print(new_post_owner)

        # Post serialization
        original_post_response = jsonable_encoder(original_post)
        original_post_response["user"] = jsonable_encoder(original_post_owner)

        new_post_response = jsonable_encoder(new_post)
        new_post_response["user"] = jsonable_encoder(new_post_owner)
        new_post_response["post"] = original_post_response

        return RepostResponse(**new_post_response)


post_service = PostService()
