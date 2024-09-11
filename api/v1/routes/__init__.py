from fastapi import APIRouter
from api.v1.routes.auth import auth
from api.v1.routes.user import users
from api.v1.routes.post import posts
from api.v1.routes.post_comment import comments
from api.v1.routes.notification import notifications

# version 1 routes

version_one = APIRouter(prefix="/api/v1")

version_one.include_router(auth)
version_one.include_router(users)
version_one.include_router(posts)
version_one.include_router(comments)
version_one.include_router(notifications)
