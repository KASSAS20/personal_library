from fastapi import FastAPI
from app.components.auth.auth import router as auth
from app.components.book.book import router as book

app = FastAPI()


# тестовый роутер для демонстрации работы API
@app.get("/")
async def root():
    return {"message": "Привет, мир!"}

# интегрирование маршрутизаторов в основой файл проекта
app.include_router(auth)
app.include_router(book)
