from fastapi import Depends, HTTPException, UploadFile
from app.database import UserConnect, BookConnect
from app.components.auth import jwt_decode
from datetime import datetime, timezone
from app.components.auth import oauth2
from app.models import BookModel
from app.router import router
from typing import Annotated
from re import sub
import aiofiles
import mammoth
import io


router = router
connect = BookConnect()


# конвертируем разметку docx в разметку md
async def docx_to_md(file):
    docx_content = await file.read()
    docx_file = io.BytesIO(docx_content)
    md_content = mammoth.convert_to_markdown(docx_file).value
    return md_content


# исправляем артефакты mammoth
async def formatter(text: str) -> str:
    text = text.replace(' __', '__').replace('__ ', '__')
    text = text.replace(' *', '*').replace('* ', '*')
    text = text.replace(' \\', '\\').replace('\\ ', '\\').replace('\\', ' \\')
    text = sub(r'__(.*?)__', lambda match: f' __{match.group(1)}__ ', text)
    text = sub(r'\*(.*?)\*', lambda match: f' *{match.group(1)}* ', text)
    return text


# роутер добавления книги
@router.post("/add_book")
async def add_book(file: UploadFile, token: Annotated[oauth2, Depends()]) -> str or HTTPException:
    if file.filename.endswith('.docx'):
        login = jwt_decode(token, 'bratislava')['login']
        id_user = await UserConnect().get_id_by_username(login)
        filename = file.filename.replace('docx', 'md')
        filepath = f'src/book/{filename}'

        content = await docx_to_md(file)
        async with aiofiles.open(filepath, 'w+') as md_file:
            text = await formatter(content)
            await md_file.write(text)

        new_book = BookModel(name=filename,
                             id_user=id_user,
                             created_at=datetime.now(timezone.utc),
                             edit_at=datetime.now(timezone.utc)
                             )
        await connect.add_book(book=new_book)
        return f'Book: {filename}'
    raise HTTPException(status_code=400, detail="Only .docx files are allowed")


# роутер получения пути к файлу по его имени
@router.get("/get_book")
async def get_book(title: str, token: Annotated[oauth2, Depends()]) -> str or HTTPException:
    login = jwt_decode(token, 'bratislava')['login']
    user_id = await UserConnect().get_id_by_username(login)
    path = await connect.get_book(title, user_id)
    if path:
        return path
    raise HTTPException(status_code=400, detail="Incorrect data")
