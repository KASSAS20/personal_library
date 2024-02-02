from fastapi import FastAPI

app = FastAPI(title='Library')


@app.get("/")
def read_root():
    return {"Hello": "World"}


# sqlalchemy = "^1.4"
# psycopg2 = "^2.9"
