from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.parser import parse_text
from app.schemas import CvParseResponse, EmbeddingRequest, EmbeddingResponse
from sentence_transformers import SentenceTransformer
import io
import fitz
import io
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(
    title="CV Parser Service API",
    version="1.0.0"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

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


@app.post("/api/v1/embed", response_model=EmbeddingResponse)
async def embed_description(request: EmbeddingRequest):
    embedding = model.encode(request.description).tolist()
    return EmbeddingResponse(description=request.description, embedding=embedding)
