from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.models import Base, UserModel, BookModel
from app.schemes import UserSchema, BookSchema
from contextlib import asynccontextmanager
from typing import NoReturn, Generator
from settings import settings
from sqlalchemy import select


# Создаём кастомный класс для асинхронного контекстного менеджера
class Connect:
    async def __aenter__(self):
        self.engine = create_async_engine(
            f'postgresql+asyncpg://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB}')
        Base.metadata.bind = self.engine
        self.maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = self.maker()
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


# декоратор служит для обозначения функции как асинхронного контекстного менеджера
@asynccontextmanager
async def get_session() -> Generator:
    async with Connect() as connection:
        yield connection


# Класс для работы с запросами к базе данных касающихся пользователей
class UserConnect:
    async def create_user(self, user: UserSchema) -> NoReturn:
        async with get_session() as session:
            async with session.begin():
                session.add(user)

    async def search_user(self, user: UserSchema) -> UserModel:
        async with get_session() as session:
            result = await session.execute(select(UserModel).filter_by(login=user.login))
            user_instance = result.scalar_one_or_none()
            return user_instance

    async def check_login(self: object, username: str) -> UserModel:
        async with get_session() as session:
            result = await session.execute(select(UserModel).filter_by(login=username))
            user_instance = result.scalars().first()
            return user_instance

    async def get_id_by_username(self, login: str):
        async with get_session() as session:
            result = await session.execute(select(UserModel).filter_by(login=login))
            result = result.scalars().first().id
            return result


# Класс для работы с запросами к базе данных касающихся книг
class BookConnect:
    async def add_book(self, book: BookSchema) -> NoReturn:
        async with get_session() as session:
            async with session.begin():
                session.add(book)


    async def get_book(self, title: str, user_id: int) -> str or bool:
        async with get_session() as session:
            search_entry = await session.execute(select(BookModel).filter_by(name=title))
            search_entry = search_entry.scalars().first()
            if search_entry:
                if search_entry.id_user == user_id:
                    path = f'src/book/{search_entry.name}'
                    return path
            return False



