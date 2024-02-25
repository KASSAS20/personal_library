from fastapi import Depends, HTTPException, File, UploadFile
from app.router import router
from app.components.auth import oauth2
from typing import Annotated
from re import sub
import mammoth
import aiofiles
import io

router = router


async def docx_to_md(file):
    docx_content = await file.read()
    docx_file = io.BytesIO(docx_content)
    md_content = mammoth.convert_to_markdown(docx_file).value
    md_filename = f'src/book/{file.filename.replace('docx', 'md')}'
    return md_filename, md_content


async def formatter(text: str) -> str:
    text = text.replace(' __', '__').replace('__ ', '__')
    text = text.replace(' *', '*').replace('* ', '*')
    text = text.replace(' \\', '\\').replace('\\ ','\\').replace('\\', ' \\')
    text = sub(r'__(.*?)__', lambda match: f' __{match.group(1)}__ ', text)
    text = sub(r'\*(.*?)\*', lambda match: f' *{match.group(1)}* ', text)
    return text

@router.post("/upload_file")
async def create_upload_file(file: UploadFile, token: Annotated[oauth2, Depends()]):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only .docx files are allowed")
    filename, content = await docx_to_md(file)
    async with aiofiles.open(filename, 'w+') as md_file:
        text = await formatter(content)
        await md_file.write(text)
    return {"filename": filename}



# Тестовый роутер для демонстрации работы OAuth2
# @router.get("/test")
# async def test(token: Annotated[oauth2, Depends()]):
#     return token