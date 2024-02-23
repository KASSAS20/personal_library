from pydantic import field_validator, BaseModel


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
