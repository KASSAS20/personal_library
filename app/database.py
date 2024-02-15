from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from app.shemes import Base


def session():
    engine = create_engine(f'postgresql://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB}')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    connect = DBSession()
    return connect
