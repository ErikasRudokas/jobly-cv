from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.parser import parse_text
from app.schemas import CvParseResponse
import io
import fitz
import io

app = FastAPI(
    title="CV Parser Service API",
    version="1.0.0"
)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return " ".join(text.split())

@app.post("/api/v1/parse/cv", response_model=CvParseResponse)
async def parse_cv(file: UploadFile = File(...)):

    if not file.filename.endswith((".pdf")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    contents = await file.read()

    text = extract_text_from_pdf(contents)

    result = parse_text(text)
    return result
