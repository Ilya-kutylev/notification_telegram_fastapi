from asyncio.log import logger

from aiogram import Bot
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from app.db.database import get_session
from app.db.models import Notification
from app.config import bot_settings
from app.services.kafka_service import KafkaService

bot = Bot(token=bot_settings.token_telegram_url)


async def process_notification(message: dict, session: AsyncSession):
    notification_id = message['notification_id']

    result = await session.execute(select(Notification).where(Notification.id == notification_id))
    notification = result.scalars().one_or_none()

    if not notification:
        return f"Уведомление с id {notification_id} не найдено"

    if notification.status == 'Delivered':
        return f"Уведомление {notification_id} уже доставлено"

    try:
        await bot.send_message(chat_id=message['user_id'], text=message['message'])
        notification.status = 'Delivered'
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        notification.status = 'Failure'

    await session.commit()


async def kafka_consumer(kafka_service: KafkaService, session: AsyncSession = Depends(get_session)):
    await kafka_service.start_consumer(lambda msg: process_notification(msg, session))