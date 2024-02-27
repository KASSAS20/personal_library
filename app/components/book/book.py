from fastapi import Depends, HTTPException, UploadFile
from app.components.auth.utils import UserConnect
from app.components.book.utils import BookConnect
from app.components.auth.auth import jwt_decode
from datetime import datetime, timezone
from app.components.auth.auth import oauth2
from app.components.book.models import BookModel
from app.router import router
from typing import Annotated
from re import sub
import aiofiles
import mammoth
import io


router = router
connect = BookConnect()


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
