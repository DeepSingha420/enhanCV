import fitz
import pymupdf4llm
import pymupdf.layout


def ResumeReader(path: str) -> str:

    upload = path

    file_bytes = upload.read()
    
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")

    return pymupdf4llm.to_markdown(doc)
