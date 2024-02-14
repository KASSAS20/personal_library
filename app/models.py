from datetime import timezone, datetime, timedelta

from pydantic import field_validator, BaseModel


class UserModel(BaseModel):
    login: str
    password: str

    @field_validator("login")
    def login_len(cls, v):
        if len(v) < 3:
            return False
        return v

    @field_validator("password")
    def passwort_len(cls, v):
        if len(v) < 8:
            return False
        return v


class UserRegistration(UserModel):
    create_at: datetime = datetime.now(timezone.utc)+timedelta(seconds=604800)


