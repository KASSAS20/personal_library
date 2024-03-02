from app.session import get_async_session
from typing import AsyncGenerator


# проверяем что мы получаем асинхронную сессию
def test_get_session():
    assert isinstance(get_async_session(), AsyncGenerator)


