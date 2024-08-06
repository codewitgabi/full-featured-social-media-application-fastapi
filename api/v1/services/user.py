from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

from api.v1.models.access_token import AccessToken

load_dotenv()
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from api.v1.models.user import User
from api.v1.schemas.user import UserCreate, UserCreateResponse

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
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

        # generate access token

        token = self.generate_access_token({"id": user.id})

        # store access toke to database

        access_token = AccessToken(
            user_id=user.id,
            token=token.get("token"),
            expiry_time=token.get("expiry_time"),
        )

        db.add(access_token)
        db.commit()
        db.refresh(access_token)

        response = UserCreateResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            access_token=str(access_token),
        )

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

    def generate_access_token(self, payload: dict):
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload.update({"exp": expire})
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"token": token, "expiry_time": expire}


user_service = UserService()
