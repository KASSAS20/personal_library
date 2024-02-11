from datetime import datetime, timezone
from fastapi import FastAPI, Response, Request
from models import User, UserModel, Base, UserRegistration
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import jwt
import hashlib

app = FastAPI(title='Library')
engine = create_engine('postgresql://sas:bratislava@postgres:5432/library')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

session = Session()


# функция хеширования пароля
def hashing(data: str):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    hashing_data = sha256_hash.hexdigest()
    return hashing_data


def get_cookie(request, key='secret_key'):
    cookies = request.cookies
    jwt_token = cookies.get('jwt_library')
    check_jwt = True if jwt_token is not None else False
    if check_jwt:
        decoded_token = jwt.decode(jwt_token, key, algorithms=['HS256'])
        real_time = int(datetime.now(timezone.utc).timestamp())
        payload = decoded_token.get('payload')
        name = payload['name']
        iat = payload['iat']
        user_found = session.query(User).filter(User.login == str(name)).first()
        if real_time <= int(iat) and user_found:
            return True
    return False


def set_cookie(response: Response, data: dict, key='secret_key'):
    jwt_token = jwt.encode(data, key, algorithm='HS256')
    response.set_cookie(key='jwt_library', value=jwt_token)


@app.post("/auth/register/")
async def register(user: UserRegistration):
    login = user.login
    password = user.password
    create_at = user.create_at

    # Проверка наличия пользователя в базе данных
    user_found = session.query(User).filter(User.login == login).first()

    if not user_found and login and password:
        # Хеширование пароля
        hashed_password = hashing(password)

        # Создание нового пользователя
        new_user = User(login=login, hash_password=hashed_password, create_at=create_at)
        session.add(new_user)
        session.commit()

        return {'registration': True}
    return {'registration': False}


@app.post("/auth/login/")
async def login(response: Response, request: Request, user: UserModel = None):
    cookie = get_cookie(request=request)
    if cookie:
        return {
            'accept': True
        }
    if user is not None:
        user_found = session.query(User).filter(
            and_(User.login == user.login, User.hash_password == hashing(user.password))).first()
        if user_found is not None:
            data = {
                'payload': {
                    'name': user.login,
                    'iat': int(datetime.now(timezone.utc).timestamp())
                }
            }
            set_cookie(response=response, data=data)
            return {
                'accept': True
            }
    return {
        'accept': False
    }


@app.post("/auth/logout")
async def logout(response: Response):
    response.set_cookie(key='jwt_library', value='')
