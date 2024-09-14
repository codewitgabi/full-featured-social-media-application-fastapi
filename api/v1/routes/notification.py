from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from api.v1.models.user import User
from api.v1.services.user import user_service
from api.v1.services.notification import notification_service
from api.v1.utils.dependencies import get_db
from api.v1.responses.success_response import success_response
from typing import List

notifications = APIRouter(prefix="/notifications", tags=["notification"])


@notifications.get("/sse")
async def sse_endpoint(user: User = Depends(user_service.get_current_user)):
    return StreamingResponse(
        notification_service.event_generator(user.id), media_type="text/event_stream"
    )


@notifications.get("")
async def user_notifications(
    user: User = Depends(user_service.get_current_user), db: Session = Depends(get_db)
):

    notifications: List = notification_service.notifications(user=user, db=db)

    return success_response(
        status_code=200,
        message="Notifications returned successfully",
        data=notifications,
    )
