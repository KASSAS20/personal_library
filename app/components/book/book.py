from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.auth.service import jwt_decode
import app.components.auth.utils as UserConnect
import app.components.book.utils as connect
from datetime import datetime, timezone
from app.components.auth.auth import oauth2
from typing import Annotated
from app.components.book.service import save_md_to_src, docx_to_md
from app.session import get_async_session
from fastapi import APIRouter


router = APIRouter(prefix='/book')


# добавление книги в бд и перевод её в md-формат
@router.post("/add")
async def add_book(file: UploadFile, token: Annotated[oauth2, Depends()],
                   session: AsyncSession = Depends(get_async_session)) -> dict:
    if file.content_type[-4:] == 'docx':
        name = ''.join(file.filename.split('.')[:-1])
        md_text = await docx_to_md(file)
        await save_md_to_src(md_text, name)
        login = jwt_decode(token)['login']
        user = await UserConnect.search_user(login, session)
        new_book = {
            'name': name,
            'user_id': user.id,
            'created_at': datetime.now(timezone.utc),
            'edit_at': datetime.now(timezone.utc)
        }
        await connect.add_book(data_book=new_book, session=session)
        return {'filename': f'{name}.md'}
    raise HTTPException(status_code=400, detail="Incorrect data")


# вывод всех книг пользователя с id и name
@router.get("/get_list")
async def get_list_book(token: Annotated[oauth2, Depends()],
                        session: AsyncSession = Depends(get_async_session)) -> dict:
    login = jwt_decode(token)['login']
    user = await UserConnect.search_user(login, session)
    user_id = user.id
    result = await connect.get_list_book_by_user_id(user_id, session)
    return result


# получение пути к книге по её name
@router.get("/get")
async def get_book(id_book: int, token: Annotated[oauth2, Depends()],
                   session: AsyncSession = Depends(get_async_session)) -> str:
    result = await connect.get_book(id_book, session)
    if result:
        return result
    raise HTTPException(status_code=400, detail="Incorrect data")
