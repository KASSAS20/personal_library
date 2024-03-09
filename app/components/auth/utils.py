from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.auth.models import UserModel
from app.components.auth.schemes import UserOut


# добавление пользователя в бд
async def create_user(data_user: dict, session: AsyncSession) -> None:
    user = UserModel(login=data_user['login'],
                     hash_password=data_user['hash_password'],
                     created_at=data_user['created_at']
                     )
    session.add(user)
    await session.commit()


# поиск пользователя
async def search_user(username: str, session: AsyncSession) -> UserOut | None:
    result = await session.execute(select(UserModel).filter_by(login=username))
    user_instance = result.scalar_one_or_none()
    if not user_instance:
        return None
    result = UserOut(
        id=user_instance.id,
        login=user_instance.login,
        hash_password=user_instance.hash_password
    )
    return result


# проверка пароля на валидность
async def check_login(username: str, session: AsyncSession) -> bool:
    if await search_user(username, session):
        return True
    return False
