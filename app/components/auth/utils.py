from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.auth.models import UserModel
from app.components.auth.schemes import UserSchema


# Класс для работы с запросами к базе данных касающихся пользователей
class UserConnect:
    @staticmethod
    async def create_user(user: UserSchema, session: AsyncSession) -> None:
        session.add(user)

    @staticmethod
    async def search_user(user: UserSchema, session: AsyncSession) -> UserModel:
        result = await session.execute(select(UserModel).filter_by(login=user.login))
        user_instance = result.scalar_one_or_none()
        return user_instance

    @staticmethod
    async def check_login(username: str, session: AsyncSession) -> UserModel:
        result = await session.execute(select(UserModel).filter_by(login=username))
        user_instance = result.scalars().first()
        return user_instance

    @staticmethod
    async def get_id_by_username(login: str, session: AsyncSession):
        result = await session.execute(select(UserModel).filter_by(login=login))
        result = result.scalars().first().id
        return result