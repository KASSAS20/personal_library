from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from app.database import Connect
from app.models import UserModel
from settings import settings
from app.shemes import User
from typing import Optional, Annotated
from jwt import PyJWTError
import bcrypt
import jwt


router = APIRouter()
connect = Connect()
oauth2 = OAuth2PasswordBearer(tokenUrl="/token")


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


def get_jwt(data, key):
    jwt_token = jwt.encode(data, key, algorithm='HS256')
    return jwt_token


def jwt_decode(token, key):
  return jwt.decode(jwt=token, key=key, algorithms='HS256')


async def get_current_user(token: str = Depends(oauth2)) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(token, settings.KEY)
        login: str = payload.get("login")
        if login is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return User(login=login)


@router.post("/registration")
async def registration(user: UserModel):
    if user.password and user.login:
        user_found = connect.search_user(user)
        if user_found is None:
            new_user = User(login=user.login,
                            hash_password=get_hashed_password(user.password).decode(),
                            created_at=datetime.now(timezone.utc)
                            )
            connect.create_user(user=new_user)
            return {
                'accept': True
            }
    return {
        'accept': False
    }


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_found = connect.check_login(username=form_data.username)
    if not user_found:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password = check_password(form_data.password, user_found.hash_password.encode())
    if not password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    new_token = get_jwt({'login': form_data.username}, settings.KEY)
    return {'access_token': new_token, 'token_type': "bearer"}
