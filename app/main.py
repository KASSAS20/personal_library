from fastapi import FastAPI

app = FastAPI()


@app.get("/registration")
async def registration():
    pass