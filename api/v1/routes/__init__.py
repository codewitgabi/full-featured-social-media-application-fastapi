from fastapi import APIRouter
from api.v1.routes.auth import auth
from api.v1.routes.user import users


# version 1 routes

version_one = APIRouter(prefix="/api/v1")

version_one.include_router(auth)
version_one.include_router(users)
