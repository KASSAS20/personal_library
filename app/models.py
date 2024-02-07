from sqlalchemy import MetaData
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    hash_password = Column(String, nullable=False)
    create_at = Column(String, nullable=False)


class UserModel(BaseModel):
    login: str
    hash_password: str
    create_at: str = None
