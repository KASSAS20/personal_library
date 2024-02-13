from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
