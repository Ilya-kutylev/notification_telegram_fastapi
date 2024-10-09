from fastapi import BackgroundTasks, Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models import Notification
from app.services.kafka_service import KafkaService, get_kafka_service

router_notification = APIRouter()


class NotificationCreate(BaseModel):
    user_id: int
    message: str


@router_notification.post("/notifications/")
async def create_notification(notification: NotificationCreate,
                              background_tasks: BackgroundTasks,
                              session: AsyncSession = Depends(get_session),
                              kafka_service: KafkaService = Depends(get_kafka_service)):
    new_notification = Notification(
        user_id=notification.user_id,
        message=notification.message
    )

    session.add(new_notification)
    await session.commit()
    await session.refresh(new_notification)

    message = {
        'notification_id': new_notification.id,
        'user_id': notification.user_id,
        'message': notification.message,
    }

    background_tasks.add_task(kafka_service.send_message, message)

    return {'status': "Notification created", 'notification_id': new_notification.id}
