from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.components.book.models import BookModel
from app.components.book.schemes import BookSchema


# Класс для работы с запросами к базе данных касающихся книг
class BookConnect:
    @staticmethod
    async def add_book(book: BookSchema, session: AsyncSession) -> None:
        session.add(book)

    @staticmethod
    async def get_book(title: str, user_id: int, session: AsyncSession) -> str or bool:
        search_entry = await session.execute(select(BookModel).filter_by(name=title))
        search_entry = search_entry.scalars().first()
        if search_entry:
            if search_entry.user_id == user_id:
                path = f'src/book/{search_entry.name}'
                return path
        return False
