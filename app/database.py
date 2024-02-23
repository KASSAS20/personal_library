from contextlib import asynccontextmanager

from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from app.models import Base, UserModel


class Connect:
    async def __aenter__(self):
        self.engine = create_async_engine(f'postgresql+asyncpg://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB}')
        self.maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = self.maker()
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


@asynccontextmanager
async def get_session():
    async with Connect() as connection:
        yield connection


class UserConnect:
    async def create_user(self, user):
        async with get_session() as session:
            session.add(user)
            session.commit()

    async def search_user(self, user):
        async with get_session() as session:
            result = await session.execute(select(UserModel).filter_by(login=user.login))
            user_instance = result.scalar_one_or_none()
            return user_instance

    async def check_login(self, username):
        async with get_session() as session:
            result = await session.execute(select(UserModel).filter_by(login=username))
            user_instance = result.scalars().first()
            return user_instance

