from fastapi import FastAPI, Depends
from app.auth import router as auth

app = FastAPI()


# @app.get("/")
# async def root(current_user: Annotated[User, Depends(get_current_user)]):
#     return {"message": "Привет, мир!"}

app.include_router(auth)
