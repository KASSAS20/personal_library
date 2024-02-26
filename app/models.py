from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import func


Base = declarative_base()


# Модель таблицы зарегистрированных пользователей
class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    hash_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


# Модель таблицы книг и их связи с таблицей пользователей
class BookModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    id_user = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    edit_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

