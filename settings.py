from pydantic_settings import BaseSettings


# схема переменного окружения
class Settings(BaseSettings):
    DB: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
