import re
from pathlib import Path

import aiofiles
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DOCS_DIR = STATIC_DIR / "docs"
OUTPUT_DIR = STATIC_DIR / "output"

DOCS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_PAGES = 500
MAX_FILE_SIZE_MB = 500
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

app = FastAPI(title="Interview Question Creator")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def sanitize_filename(name: str) -> str:
    clean_name = Path(name).name
    if not clean_name:
        return "uploaded_document.pdf"
    return clean_name


def extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages).strip()


def count_pdf_pages(file_path: Path) -> int:
    reader = PdfReader(str(file_path))
    return len(reader.pages)


def create_question_answer_pairs(text: str, limit: int = 10):
    chunks = [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment.strip()]
    pairs = []
    for index, chunk in enumerate(chunks[:limit], start=1):
        question = f"Question {index}: What is the main idea discussed in this section?"
        answer = f"Answer {index}: {chunk[:250]}"
        pairs.append(f"{question}\n{answer}\n")
    return "\n".join(pairs)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"max_pages": MAX_PAGES, "max_mb": MAX_FILE_SIZE_MB})


@app.post("/upload")
async def upload_file(pdf_file: UploadFile = File(...), filename: str = Form(...)):
    clean_name = sanitize_filename(filename)
    file_path = DOCS_DIR / clean_name

    contents = await pdf_file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File is too large (max {MAX_FILE_SIZE_MB}MB).",
        )

    async with aiofiles.open(file_path, "wb") as destination:
        await destination.write(contents)

    # Reject after saving if it has too many pages, and clean up the file.
    try:
        page_count = count_pdf_pages(file_path)
    except Exception:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Could not read this PDF. Is it valid/not password-protected?")

    if page_count > MAX_PAGES:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=f"PDF has {page_count} pages (max {MAX_PAGES}). Please upload a shorter document.",
        )

    return {"msg": "success", "pdf_filename": f"/static/docs/{clean_name}"}


@app.post("/analyze")
async def analyze_pdf(pdf_filename: str = Form(...)):
    if not pdf_filename:
        raise HTTPException(status_code=400, detail="PDF file is required")

    relative_path = pdf_filename.lstrip("/")
    file_path = (BASE_DIR / relative_path).resolve()

    if not file_path.exists() or file_path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Uploaded PDF not found")

    text = extract_pdf_text(file_path)
    if not text:
        raise HTTPException(status_code=400, detail="No readable text found in the uploaded PDF")

    output_name = f"{file_path.stem}_qa.txt"
    output_path = OUTPUT_DIR / output_name
    output_text = create_question_answer_pairs(text)

    async with aiofiles.open(output_path, "w", encoding="utf-8") as destination:
        await destination.write(output_text)

    return {"output_file": f"/static/output/{output_name}"}


@app.post("/query")
async def query_vector_store(request: Request):
    body = await request.json()
    query = (body or {}).get("query", "").strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    return {"response": f"This is a simulated response based on your query: {query}"}


if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", 8000))
    module_name = Path(__file__).stem

    print(f"Starting server — open this in your browser: http://127.0.0.1:{port}")
    uvicorn.run(f"{module_name}:app", host="0.0.0.0", port=port, reload=True)