from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.auth.models import UserModel
from app.components.auth.schemes import UserSchema


# добавление пользователя в бд
async def create_user(data_user: dict, session: AsyncSession) -> None:
    user = UserModel(login=data_user['login'],
                     hash_password=data_user['hash_password'],
                     created_at=data_user['created_at']
                     )
    session.add(user)
    await session.commit()


# поиск пользователя
async def search_user(username: str, session: AsyncSession) -> UserModel:
    result = await session.execute(select(UserModel).filter_by(login=username))
    user_instance = result.scalar_one_or_none()
    return user_instance


# проверка пароля на валидность
async def check_login(username: str, session: AsyncSession) -> bool:
    if await search_user(username, session):
        return True
    return False
