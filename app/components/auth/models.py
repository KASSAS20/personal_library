from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.models import Base


# Модель таблицы зарегистрированных пользователей
class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    hash_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
