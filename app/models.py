from sqlalchemy import MetaData  # , Table, Column, Integer, String
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    hash_password = Column(String, nullable=False)


class UserModel(BaseModel):
    login: str
    hash_password: str