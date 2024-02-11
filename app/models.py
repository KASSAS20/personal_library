from pydantic import BaseModel, field_validator
from sqlalchemy import Column, String
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    hash_password = Column(String, nullable=False)
    create_at = Column(String, nullable=False)


class UserModel(BaseModel):
    login: str
    password: str

    @field_validator("login")
    def login_len(cls, v):
        if len(v) < 3:
            return False
        return v

    @field_validator("password")
    def passwort_len(cls, v):
        if len(v) < 8:
            return False
        return v


class UserRegistration(UserModel):
    create_at: str = str(datetime.now(timezone.utc))[:10]



