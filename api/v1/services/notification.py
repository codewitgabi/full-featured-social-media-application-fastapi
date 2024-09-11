from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict
import asyncio
from api.v1.models.user import User
from api.v1.models.notification import Notification


class NotificationService:

    user_event_queues: Dict[str, asyncio.Queue] = {}

    async def event_generator(user_id: str):
        if user_id not in user_event_queues:
            user_event_queues[user_id] = asyncio.Queue()
        
        while True:
            event = await user_event_queues[user_id].get()
            yield f"data: {event}"


    def notifications(self, user: User, db: Session):
        notifications = db.query(Notification).filter(Notification.user_id==user.id).all()

        return notifications

notification_service = NotificationService()
