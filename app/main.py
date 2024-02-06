from fastapi import FastAPI
# import JWT
from models import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI(title='Library')
engine = create_engine('postgresql://sas:bratislava@postgres:5432/library')
Session = sessionmaker(bind=engine)
try:
    Base.metadata.create_all(engine)
except:
    pass

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/register/{login}/{password}")
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
