from datetime import datetime, timezone, timedelta

from fastapi import APIRouter
import bcrypt
from app.models import UserModel
from app.shemes import User
from app.database import session

router = APIRouter()
connect = session()


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


@router.post("/registration")
async def registration(user: UserModel):
    if user.password and user.login:
        connection = session()
        user_found = connection.query(User).filter(User.login == user.login).first()
        if user_found is None:
            new_user = User(login=user.login,
                            hash_password=get_hashed_password(user.password).decode(),
                            created_at=datetime.now(timezone.utc)+timedelta(seconds=604800)
                            )
            connect.add(new_user)
            connect.commit()
            connect.close()
            return True
    return False


@router.post("/login")
async def login(user: UserModel):
    connection = session()
    user_found = connection.query(User).filter_by(login=user.login).first()
    connection.close()
    if user.password and user.login and user_found is not None:
        password = check_password(user.password, user_found.hash_password.encode())
        return password
    return False
