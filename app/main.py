from fastapi import FastAPI, Response, Request
from models import User, UserModel, Base
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import JWT
import hashlib

app = FastAPI(title='Library')
engine = create_engine('postgresql://sas:bratislava@postgres:5432/library')
Session = sessionmaker(bind=engine)
# Создание таблиц по моделям из models.py
Base.metadata.create_all(engine)

session = Session()


# функция хеширования пароля
def hash_pass(password: str):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    password = sha256_hash.hexdigest()
    return password


# Проверка jwt-токена на валидность
def validation_user(jwt: str, session=session):
    try:
        parse_jwt = JWT.decode_jwt(jwt)
        login = str(parse_jwt['login'])
        password = str(parse_jwt['hash_password'])
        user_found = session.query(User).filter(and_(User.login == login, User.password == password)).first()
        # Если пользователь не найден
        if user_found is None:
            return False
        else:
            return True
    except Exception as _ex:
        print(f'error: {_ex}')
    finally:
        session.commit()
        session.close()


@app.post("/auth/register/")
async def register(login: str, password: str):
    try:
        # проверяем есть ли пользователь с таким именем
        user_found = session.query(User).filter(User.login == login).first()
        if user_found is None:
            if len(login) < 3:
                return {
                    'error': 'login length is less than 3 characters'
                }
            elif len(password) < 8:
                return {
                    'error': 'password length is less than 8 characters'
                }
            dt = datetime.utcnow()
            dt_utc = dt.astimezone(timezone.utc)
            date_utc = str(dt_utc.date())
            password = hash_pass(password)
            user_model = UserModel.parse_obj({
                'login': login,
                'hash_password': password,
                'create_at': date_utc
            })
            new_user = User(
                login=user_model.login,
                hash_password=user_model.hash_password,
                create_at=user_model.create_at
            )
            session.add(new_user)
            session.commit()
        else:
            return {'error': 'there is already a user with that name'}
    except Exception as _ex:
        # при ошибке откатываем изменение бд
        session.rollback()
        return {'error': _ex}
    finally:
        session.close()


@app.get("/auth/login/")
async def login(response: Response, request: Request, login: str, password: str):
    cookies = request.cookies
    jwt_token = cookies.get('jwt_library')
    check_user = validation_user(jwt_token)
    password = hash_pass(password)
    # Если куки не найдены или не валидны(истек срок или пользователь не найден)
    if cookies == {} or not check_user:
        try:
            # находим пользователя по имени и паролю, иначе None
            user_found = session.query(User).filter(and_(User.login == login, User.hash_password == password)).first()
            # Если пользователь не найден генерируем jwt и записываем в cookie
            if user_found is None:
                return {'access': False}
            else:
                user_model = UserModel.parse_obj({'login': login, 'hash_password': password})
                jwt = JWT.generate_jwt(login=user_model.login, password=user_model.hash_password)
                response.set_cookie(key='jwt_library', value=jwt['access_token'])
                return {
                    'access': True,
                    'jwt': jwt
                }
        except Exception as _ex:
            # при ошибке откатываем изменение бд
            session.rollback()
            return {'2error': _ex}
        finally:
            session.close()
    else:
        return {'access': True}


@app.post("/auth/logout")
async def logout(response: Response):
    response.set_cookie(key='jwt_library', value='')
