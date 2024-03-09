from fastapi import FastAPI
from app.components.auth.auth import router as auth
from app.components.book.book import router as book

app = FastAPI()


# интегрирование маршрутизаторов в основой файл проекта
app.include_router(auth)
app.include_router(book)
