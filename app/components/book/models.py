from app.models import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func


# Модель таблицы книг и их связи с таблицей пользователей
class BookModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    edit_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

