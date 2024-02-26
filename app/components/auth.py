from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from datetime import datetime, timezone
from app.database import UserConnect
from app.schemes import UserSchema
from app.models import UserModel
from app.router import router
from settings import settings
from typing import Annotated
import bcrypt
import jwt

router = router
connect = UserConnect()
oauth2 = OAuth2PasswordBearer(tokenUrl="/token")


# Функция для хеширования пароля с добавлением соли
def get_hashed_password(plain_text_password: str) -> bytes:
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


# сравнение пароля с хэшированным паролем из бд
def check_password(plain_text_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


# генерация JWT
def get_jwt(data: dict, key: str) -> str:
    jwt_token = jwt.encode(data, key, algorithm='HS256')
    return jwt_token


# Декодирование JWT
def jwt_decode(token: dict, key: str) -> dict:
    return jwt.decode(jwt=token, key=key, algorithms='HS256')


# Роутер регистрации новых пользователей
@router.post("/registration")
async def registration(user: UserSchema) -> dict or HTTPException:
    if user.password and user.login:
        user_found = await connect.search_user(user)
        if user_found is None:
            new_user = UserModel(login=user.login,
                                 hash_password=get_hashed_password(user.password).decode(),
                                 created_at=datetime.now(timezone.utc)
                                 )
            await connect.create_user(new_user)
            return {
                'accept': True
            }
    raise HTTPException(status_code=400, detail="Incorrect data")


# роутер привязанный к oauth2 для предоставления доступа в случаи корректного ввода данных
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict or HTTPException:
    user_found = await connect.check_login(username=form_data.username)
    if not user_found:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password = check_password(form_data.password, user_found.hash_password.encode())
    if not password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    new_token = get_jwt({'login': form_data.username}, settings.KEY)
    return {'access_token': new_token, 'token_type': "bearer"}
