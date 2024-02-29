from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.book.models import BookModel
from app.components.book.schemes import BookSchema


async def add_book(book: BookSchema, session: AsyncSession) -> None:
    session.add(book)
    await session.commit()


async def get_book(book_id: int, session: AsyncSession) -> str | None:
    search_entry = await session.execute(select(BookModel).filter_by(id=book_id))
    search_entry = search_entry.scalars().first()
    if search_entry:
        path = f'src/book/{search_entry.name}'
        return path


async def get_list_book_by_user_id(user_id: int, session: AsyncSession) -> dict | None:
    query = text("SELECT * FROM books WHERE user_id = :user_id")
    result = await session.execute(query, {"user_id": user_id})
    books_list = [[book.name, book.id] for book in result]
    result = {i[1]: i[0] for i in books_list}
    return result
