from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TIMESTAMP
from settings import settings
from sqlalchemy import func


Base = declarative_base()


# Модель таблицы зарегистрированных пользователей
class UserModel(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    hash_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now() + timedelta(seconds=settings.WEEK_TO_SECOND))
