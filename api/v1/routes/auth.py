from fastapi import APIRouter, Depends, status
from api.v1.responses.success_response import success_response
from api.v1.schemas.user import UserCreate, UserCreateResponse
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
