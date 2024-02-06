from sqlalchemy import MetaData  # , Table, Column, Integer, String
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
