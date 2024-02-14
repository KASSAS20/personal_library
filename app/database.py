from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.shemes import Base


def session():
    engine = create_engine('ваша_строка_подключения_к_базе_данных')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    connect = DBSession()
    return connect
