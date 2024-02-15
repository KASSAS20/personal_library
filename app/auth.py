from datetime import datetime, timezone, timedelta

from fastapi import APIRouter
from app.models import UserModel
from app.shemes import User
from app.database import session

router = APIRouter()
connect = session()

# сделать хеширование пароля при добавлении в бд

@router.post("/registration")
async def registration(user: UserModel):
    if user.password and user.login:
        connection = session()
        user_found = connection.query(User).filter(User.login == user.login).first()
        if user_found is None:
            new_user = User(login=user.login,
                            hash_password=user.password,
                            created_at=datetime.now(timezone.utc)+timedelta(seconds=604800)
                            )
            connect.add(new_user)
            connect.commit()
            connect.close()
            return True
    return False
