from fastapi import FastAPI
# import JWT
from models import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title='Library')
engine = create_engine('postgresql://sas:bratislava@postgres:5432/library')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/register/{login}/{password}")
def register(login: str, password: str):
    session = Session()
    try:
        new_user = User(login=login, password=password)
        session.add(new_user)
        session.commit()
        session.close()
    except SQLAlchemyError:
        session.rollback()
    finally:
        session.close()
