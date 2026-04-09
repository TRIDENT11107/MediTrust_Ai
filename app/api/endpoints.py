# app/api/endpoints.py
from fastapi import APIRouter, UploadFile, File, Query
from app.core.pipeline import MediTrustPipeline

router = APIRouter()
_pipeline = MediTrustPipeline()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/process")
async def process_document(
    file: UploadFile = File(...),
    policy: str = Query("default")
):
    """
    Upload a document image or PDF, apply OCR+PII+redaction, and return result metadata.
    """
    return await _pipeline.process_document(file, policy)
