from fastapi import FastAPI
from app.auth import router as auth

app = FastAPI()


# тестовый роутер для демонстрации работы API
@app.get("/")
async def root():
    return {"message": "Привет, мир!"}

# интегрирование маршрутизатора в основой файл проекта
app.include_router(auth)
