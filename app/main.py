from fastapi import FastAPI, Response, Request
import JWT
from models import User, Base
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

app = FastAPI(title='Library')
engine = create_engine('postgresql://sas:bratislava@postgres:5432/library')
Session = sessionmaker(bind=engine)
# Создание таблиц по моделям из models.py
Base.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Проверка jwt-токена на валидность
def validation_user(jwt: str):
    session = Session()
    try:
        parse_jwt = JWT.decode_jwt(jwt)
        login = str(parse_jwt['login'])
        password = str(parse_jwt['password'])
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
    session = Session()
    try:
        # проверяем есть ли пользователь с таким именем
        user_found = session.query(User).filter(User.login == login).first()
        if user_found is None:
            new_user = User(login=login, password=password)
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
    session = Session()
    jwt_token = cookies.get('jwt_library')
    check_user = validation_user(jwt_token)
    # Если куки не найдены или не валидны(истек срок или пользователь не найден)
    if cookies == {} or not check_user:
        try:
            # находим пользователя по имени и паролю, иначе None
            user_found = session.query(User).filter(and_(User.login == login, User.password == password)).first()
            # Если пользователь не найден генерируем jwt и записываем в cookie
            if user_found is not None:
                jwt = JWT.generate_jwt(login=login, password=password)
                response.set_cookie(key='jwt_library', value=jwt['access_token'])
                return {
                    'access': True,
                    'jwt': jwt
                }
            else:
                return {'access': False}
        except Exception as _ex:
            # при ошибке откатываем изменение бд
            session.rollback()
            return {'error': _ex}
        finally:
            session.close()
    else:
        return {'access': True}

@app.post("/auth/logout")
async def logout(response: Response):
    response.set_cookie(key='jwt_library', value='')