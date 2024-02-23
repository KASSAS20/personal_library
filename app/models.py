from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Модель таблицы зарегистрированных пользователей
class UserModel(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    hash_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc)+timedelta(seconds=604800))
