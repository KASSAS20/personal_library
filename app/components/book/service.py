import aiofiles
from mammoth import convert_to_html
import markdownify
import io


# перевод docx-файла в md-формат
async def docx_to_md(file) -> str:
    docx_content = await file.read()
    docx_file = io.BytesIO(docx_content)
    html = convert_to_html(docx_file).value
    md = markdownify.markdownify(html, heading_style="ATX")
    return md


async def save_md_to_src(file, name: str) -> None:
    async with aiofiles.open(f'src/book/{name}.md', 'w+') as md:
        await md.write(file)