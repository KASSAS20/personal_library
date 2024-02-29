from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.components.auth.service import jwt_decode
import app.components.auth.utils as UserConnect
import app.components.book.utils as connect
from datetime import datetime, timezone
from app.components.auth.auth import oauth2
from app.components.book.models import BookModel
from app.router import router
from typing import Annotated
from app.components.book.converter import docx_to_md
from app.components.book.service import save_md_to_src
from app.session import get_session


router = router


@router.post("/add_book")
async def add_book(file: UploadFile, token: Annotated[oauth2, Depends()], session: AsyncSession = Depends(get_session)):
    if file.content_type == 'application/wps-office.docx':
        name = ''.join(file.filename.split('.')[:-1])
        md_text = await docx_to_md(file)
        await save_md_to_src(md_text, name)
        login = jwt_decode(token, 'bratislava')['login']
        user_id = await UserConnect.get_id_by_username(login, session)
        new_book = BookModel(name=name,
                             user_id=user_id,
                             created_at=datetime.now(timezone.utc),
                             edit_at=datetime.now(timezone.utc)
                             )
        await connect.add_book(book=new_book, session=session)
        return {'filename': f'{name}.md'}
    raise HTTPException(status_code=400, detail="Incorrect data")


@router.post("/get_list_book")
async def get_list_book(token: Annotated[oauth2, Depends()], session: AsyncSession = Depends(get_session)):
    pass

#
# # роутер добавления книги
# @router.post("/add_book")
# async def add_book(file: UploadFile, token: Annotated[oauth2, Depends()]) -> str or HTTPException:
#     if file.filename.endswith('.docx'):
#         login = jwt_decode(token, 'bratislava')['login']
#         id_user = await UserConnect().get_id_by_username(login)
#         filename = file.filename.replace('docx', 'md')
#         filepath = f'src/book/{filename}'
#
#         content = await docx_to_md(file)
#         async with aiofiles.open(filepath, 'w+') as md_file:
#             text = await formatter(content)
#             await md_file.write(text)
#
#         new_book = BookModel(name=filename,
#                              id_user=id_user,
#                              created_at=datetime.now(timezone.utc),
#                              edit_at=datetime.now(timezone.utc)
#                              )
#         await connect.add_book(book=new_book)
#         return {'Book' : filename}
#     raise HTTPException(status_code=400, detail="Only .docx files are allowed")
#
#
# # роутер получения пути к файлу по его имени
# @router.get("/get_book")
# async def get_book(title: str, token: Annotated[oauth2, Depends()]) -> str or HTTPException:
#     login = jwt_decode(token, 'bratislava')['login']
#     user_id = await UserConnect().get_id_by_username(login)
#     path = await connect.get_book(title, user_id)
#     if path:
#         return path
#     raise HTTPException(status_code=400, detail="Incorrect data")
