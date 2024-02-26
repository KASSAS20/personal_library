from pydantic import field_validator, BaseModel, model_validator


# Схема данных зарегистрированных пользователей
class UserSchema(BaseModel):
    login: str
    password: str

    @field_validator("login")
    def login_len(cls, v):
        if len(v) < 3:
            return False
        return v

    @field_validator("password")
    def password_len(cls, v):
        if len(v) < 8:
            return False
        return v

    @model_validator(mode="after")
    def password_quality_login(self):
        if self.login == self.password:
            raise ValueError("password quality login")
        return self


# Схема данных добавленных книг
class BookSchema(BaseModel):
    name: str
    id_user: int
