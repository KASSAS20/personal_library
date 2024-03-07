from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.book.models import BookModel


# добавление книги в бд
async def add_book(data_book: dict, session: AsyncSession) -> None:
    book = BookModel(name=data_book['name'],
                     user_id=data_book['user_id'],
                     created_at=data_book['created_at'],
                     edit_at=data_book['edit_at']
                     )
    session.add(book)
    await session.commit()


# получение пути к книге
async def get_book(book_id: int, session: AsyncSession) -> str | None:
    search_entry = await session.execute(select(BookModel).filter_by(id=book_id))
    search_entry = search_entry.scalars().first()
    if search_entry:
        path = f'src/book/{search_entry.name}'
        return path


# получение списка книг текущего пользователя
async def get_list_book_by_user_id(user_id: int, session: AsyncSession) -> dict | None:
    stmt = select(BookModel).filter(BookModel.user_id == user_id)
    result = await session.execute(stmt)
    books_list = {book.id: book.name for book in result.scalars()}
    return books_list
