from pydantic import BaseModel


# Схема данных добавленных книг
class BookSchema(BaseModel):
    name: str
    user_id: int

