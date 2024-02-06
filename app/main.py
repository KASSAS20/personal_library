from fastapi import FastAPI
import JWT
from models import User, Base
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker



app = FastAPI(title='Library')
engine = create_engine('postgresql://sas:bratislava@postgres:5432/library')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/auth/register/{login}/{password}")
def register(login: str, password: str):
    session = Session()
    try:
        user_found = session.query(User).filter(User.login == login).first()
        if user_found is None:
            new_user = User(login=login, password=password)
            session.add(new_user)
            session.commit()

        else:
            return {'error': 'there is already a user with that name'}
    except Exception as _ex:
        session.rollback()
        return {'error': _ex}
    finally:
        session.close()


@app.get("/auth/login/{login}/{password}")
def login(login: str, password: str):
    session = Session()
    try:
        user_found = session.query(User).filter(and_(User.login == login, User.password == password)).first()
        if user_found is not None:
            jwt = JWT.generate_jwt(login=login, password=password)
            return {
                'access': True,
                'jwt': jwt
            }
        else:
            return {'access': False}
    except Exception as _ex:
        session.rollback()
        return {'error': _ex}
    finally:
        session.close()
