from fastapi import FastAPI
from app.auth import router as auth

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Привет, мир!"}

app.include_router(auth)
