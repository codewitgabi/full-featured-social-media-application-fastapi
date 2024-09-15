from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from dotenv import load_dotenv
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder

from api.v1.models.access_token import AccessToken
from api.v1.models.cover_photo import CoverPhoto
from api.v1.models.profile_picture import ProfilePicture
from api.v1.models.social_link import SocialLink
from api.v1.utils.dependencies import get_db

load_dotenv()
from fastapi import Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, text
from passlib.context import CryptContext
import jwt
from api.v1.models.user import User
from api.v1.schemas.user import UserCreate, UserUpdateSchema, UserResponse
from api.v1.utils.storage import upload
from api.v1.models.notification import Notification
from api.v1.services.notification import notification_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


class UserService:
    def create_user(self, user: UserCreate, db: Session):
        # check if user already exists

        if self.exists(user.email, db):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "User with email already exists"
            )

        hashed_password = self.hash_password(user.password)
        user.password = hashed_password
        user = User(**user.model_dump())

        db.add(user)
        db.commit()
        db.refresh(user)

        # create notification

        notification = Notification(
            user_id=user.id, message="Account created successfully"
        )

        db.add(notification)
        db.commit()

        # generate access token

        token, expiry = self.generate_access_token(db, user).values()

        user = jsonable_encoder(
            self.get_user_detail(db=db, user_id=user.id), exclude={"password"}
        )

        response = {
            "access_token": token,
            "expiry": expiry,
            "user": user,
        }

        return response

    def hash_password(self, password: str) -> str:
        return hash_context.hash(password)

    def verify_password(self, password: str, hashed_password) -> bool:
        return hash_context.verify(password, hashed_password)

    def exists(self, email: str, db: Session) -> bool:
        user = db.query(User).filter(User.email == email).first()

        if user:
            return True

        return False

    def generate_access_token(self, db: Session, user: User) -> dict:
        payload = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload.update({"exp": expire})
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # store access toke to database

        access_token = AccessToken(user_id=user.id, token=token, expiry_time=expire)

        db.add(access_token)
        db.commit()
        db.refresh(access_token)

        return {"token": token, "expiry_time": expire}

    def get_user_by_email(self, email: str, db: Session) -> User | None:
        if self.exists(email, db):
            return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, id: str, db: Session) -> User | None:
        return db.query(User).filter(User.id == id).first() or None

    def handle_login(self, db: Session, email: str, password: str):
        user = self.get_user_by_email(email, db)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No account associated with provided email",
            )

        # check if password is correct

        if not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )

        # create access token

        access_token, expiry = self.generate_access_token(db, user).values()

        # update last login

        user.last_login = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

        # create notification

        notification = Notification(user_id=user.id, message="Account Login successful")

        db.add(notification)
        db.commit()

        user = jsonable_encoder(
            self.get_user_detail(db=db, user_id=user.id), exclude={"password"}
        )

        response = {
            "access_token": access_token,
            "expiry": expiry,
            "user": user,
        }

        return response

    def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db),
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            email: str = payload.get("email")

            if not email:
                raise credential_exception

        except jwt.InvalidTokenError:
            raise credential_exception

        # check if token is blacklisted

        access_token = db.query(AccessToken).filter(AccessToken.token == token).first()

        if access_token and access_token.blacklisted:
            raise credential_exception

        user = self.get_user_by_email(email, db)

        if not user:
            raise credential_exception

        return user

    def blacklist_token(self, db: Session, user: User) -> None:
        # get user access token

        access_token = (
            db.query(AccessToken).filter(AccessToken.user_id == user.id).first()
        )

        access_token.blacklisted = True

        db.commit()
        db.refresh(access_token)

        # create notification

        notification = Notification(
            user_id=user.id, message="Account logout successful"
        )

        db.add(notification)
        db.commit()

    def get_user_detail(self, db: Session, user_id: str):
        query = (
            db.query(User)
            .options(
                joinedload(User.profile_pictures),
                joinedload(User.cover_photos),
                joinedload(User.followers),
                joinedload(User.social_links),
            )
            .filter(User.id == user_id)
            .first()
        )

        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return query

    def update_user_profile(
        self, db: Session, user: User, user_id: str, schema: UserUpdateSchema
    ):
        # verify that user is the one logged in

        if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this user",
            )

        data = schema.model_dump(exclude_unset=True)

        profile_picture = data.pop("profile_picture", None)

        if profile_picture:
            # upload image to cloudinary

            image_url = upload(profile_picture)

            # create new profile picture

            new_profile_picture = ProfilePicture(user_id=user.id, image=image_url)

            db.add(new_profile_picture)
            db.commit()
            db.refresh(new_profile_picture)

        cover_photo = data.pop("cover_photo", None)

        if cover_photo:
            # upload image to cloudinary

            image_url = upload(cover_photo)

            # create new cover photo

            new_cover_photo = CoverPhoto(user_id=user.id, image=image_url)

            db.add(new_cover_photo)
            db.commit()
            db.refresh(new_cover_photo)

        social_links = data.pop("social_links", [])

        if social_links:
            # remove all associated social links

            db.query(SocialLink).filter(SocialLink.user_id == user_id).delete()
            db.flush()

            # create new social links

            for link in social_links:
                social_link = SocialLink(link=link, user_id=user_id)

                db.add(social_link)

            db.commit()

        for key, value in data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        # create notification

        notification = Notification(
            user_id=user.id, message="Account updated successfully"
        )

        db.add(notification)
        db.commit()

        # return user detail

        return jsonable_encoder(
            self.get_user_detail(db=db, user_id=user_id), exclude={"password"}
        )

    def delete_user_profile(self, db: Session, user: User, user_id: str):
        # check if user is the currently logged in user

        if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this user",
            )

        db.delete(user)
        db.commit()

    def fetch_all(self, db: Session, search: str = ""):
        query = (
            db.query(User)
            .options(joinedload(User.profile_pictures), joinedload(User.social_links))
            .order_by(text("RANDOM()"))
        )

        if search:
            query = query.filter(
                or_(
                    User.username.icontains(f"%{search}%"),
                    User.email.icontains(f"%{search}%"),
                )
            )

        users = query.all()

        return jsonable_encoder(users, exclude={"password"})

    def follow_user(self, db: Session, user_id: str, user: User, background_task: BackgroundTasks):

        followee = db.query(User).filter(User.id == user_id).first()
        if not followee:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        if followee not in user.followings:
            user.followings.append(followee)

            notification = Notification(
                user_id=followee.id, message=f"{user.username} followed you"
            )

            db.add(notification)
            db.commit()

            background_task.add_task(notification_service.user_event_queues[notification.user_id].put, notification.message)

    def unfollow_user(self, db: Session, user_id: str, user: User, background_task: BackgroundTasks):
        user_to_unfollow = db.query(User).filter(User.id == user_id).first()

        if not user_to_unfollow:
            raise HTTPException(status_code=404, detail="User not found")

        if user_to_unfollow not in user.followings:
            raise HTTPException(
                status_code=404, detail="You are not following this user"
            )

        user.followings.remove(user_to_unfollow)

        notification = Notification(
            user_id=user_to_unfollow.id, message=f"{user.username} unfollowed you"
        )

        db.add(notification)
        db.commit()

        background_task.add_task(notification_service.user_event_queues[notification.user_id].put, notification.message)


    def followers(self, db: Session, user: User):

        followers = [
            UserResponse(**jsonable_encoder(follower)) for follower in user.followers
        ]

        return followers

    def followings(self, db: Session, user: User):

        followings = [
            UserResponse(**jsonable_encoder(following)) for following in user.followings
        ]

        return followings


user_service = UserService()
