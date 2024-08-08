from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from dotenv import load_dotenv

from api.v1.models.access_token import AccessToken

load_dotenv()
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from api.v1.models.user import User
from api.v1.schemas.user import (
    LoginResponse,
    UserCreate,
    UserCreateResponse,
    UserLoginSchema,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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

        token, expiry = self.generate_access_token(db, user).values()

        response = UserCreateResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            access_token=token,
            expiry=expiry,
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

        response = LoginResponse(
            access_token=access_token,
            expiry=expiry,
            user=UserLoginSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                bio=user.bio,
                contact_info=user.contact_info,
                social_links=user.social_links,
                role=user.role,
                last_login=user.last_login,
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
        )

        return response

    def get_current_user(
        self, db: Session, token: Annotated[str, Depends(oauth2_scheme)]
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            email: str = payload.get("email")

            if not email:
                raise credential_exception

        except jwt.InvalidTokenError:
            raise credential_exception

        user = self.get_user_by_email(email, db)

        if not user:
            raise credential_exception

        return user


user_service = UserService()
