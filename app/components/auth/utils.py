from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.auth.models import UserModel
from app.components.auth.schemes import UserSchema


# добавление пользователя в бд
async def create_user(user: UserSchema, session: AsyncSession) -> None:
    session.add(user)
    await session.commit()


# поиск пользователя
async def search_user(user: UserSchema, session: AsyncSession) -> UserModel:
    result = await session.execute(select(UserModel).filter_by(login=user.login))
    user_instance = result.scalar_one_or_none()
    return user_instance


# проверка пароля на валидность
async def check_login(username: str, session: AsyncSession) -> UserModel:
    result = await session.execute(select(UserModel).filter_by(login=username))
    user_instance = result.scalars().first()
    return user_instance


# поиск id пользователя по login
async def get_id_by_username(login: str, session: AsyncSession):
    result = await session.execute(select(UserModel).filter_by(login=login))
    result = result.scalars().first().id
    return result