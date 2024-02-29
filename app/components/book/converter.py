from mammoth import convert_to_html
import markdownify
import io


async def docx_to_md(file):
    docx_content = await file.read()
    docx_file = io.BytesIO(docx_content)
    html = convert_to_html(docx_file).value
    md = markdownify.markdownify(html, heading_style="ATX")
    return md

