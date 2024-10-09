import datetime

from sqlalchemy import func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Model = declarative_base()


class Notification(Model):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="Pending")
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
