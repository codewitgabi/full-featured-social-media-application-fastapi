from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from api.v1.responses.success_response import success_response
from api.v1.schemas.user import UserCreate, UserCreateResponse, UserLogin
from api.v1.services.user import user_service
from sqlalchemy.orm import Session

from api.v1.utils.dependencies import get_db


auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, int | str | UserCreateResponse],
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user_service.create_user(user, db)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=new_user,
    )


@auth.post("/login", status_code=status.HTTP_200_OK)
async def login(data: UserLogin, db: Session = Depends(get_db)):
    data = user_service.handle_login(db, email=data.email, password=data.password)

    return success_response(
        status_code=status.HTTP_200_OK, message="User login successful", data=jsonable_encoder(data)
    )
