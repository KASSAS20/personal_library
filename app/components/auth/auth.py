from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.auth.service import get_hashed_password, check_password, get_jwt
import app.components.auth.utils as connect
from app.components.auth.schemes import UserSchema
from app.components.auth.models import UserModel
from app.session import get_async_session
from settings import settings
from typing import Annotated
from fastapi import APIRouter


router = APIRouter(prefix='/auth')
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Роутер регистрации новых пользователей
@router.post("/registration")
async def registration(user: UserSchema,
                       session: AsyncSession = Depends(get_async_session)) -> dict:
    if user.password and user.login:
        user_found = await connect.search_user(user, session)
        if user_found is None:
            new_user = UserModel(login=user.login,
                                 hash_password=get_hashed_password(user.password).decode(),
                                 created_at=datetime.now(timezone.utc)
                                 )
            await connect.create_user(new_user, session)
            return {
                'accept': True
            }
    raise HTTPException(status_code=400, detail="Incorrect data")


# роутер привязанный к oauth2 для предоставления доступа в случаи корректного ввода данных
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: AsyncSession = Depends(get_async_session)) -> dict:
    user_found = await connect.check_login(username=form_data.username, session=session)
    if not user_found:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password = check_password(form_data.password, user_found.hash_password.encode())
    if not password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    new_token = get_jwt({'login': form_data.username}, settings.KEY)
    return {'access_token': new_token, 'token_type': "bearer"}
