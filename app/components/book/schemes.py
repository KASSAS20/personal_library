from pydantic import field_validator, BaseModel, model_validator


# Схема данных добавленных книг
class BookSchema(BaseModel):
    name: str
    user_id: int
