from datetime import datetime, timezone, timedelta

from sqlalchemy import Column, String, TIMESTAMP, DateTime, create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    hash_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc)+timedelta(seconds=604800))



