# app/core/pipeline.py
from pathlib import Path
from typing import Dict, Any, List
from fastapi import UploadFile

from app.core.config import OUTPUT_DIR
from app.utils.file_handler import save_upload, ensure_image, static_url
from app.models.ocr_processor import run_ocr
from app.models.pii_detector import find_pii
from app.models.signature_detector import detect_signatures
from app.models.redaction_engine import redact

class MediTrustPipeline:
    def __init__(self) -> None:
        pass

    async def process_document(self, file: UploadFile, policy: str) -> Dict[str, Any]:
        # 1) Save upload
        saved = await save_upload(file)
        # 2) Prepare a working image (leave PDF as-is)
        work = ensure_image(saved)

        # 3) OCR (skip for PDFs)
        ocr = {"text": "", "words": []}
        if work.suffix.lower() != ".pdf":
            ocr = run_ocr(work)

        # 4) PII from OCR text
        pii_items = find_pii(ocr.get("text", "")) if ocr.get("text") else []

        # 5) Detection: signatures + exact-word matches for PII terms
        boxes: List[List[int]] = []
        if work.suffix.lower() != ".pdf":
            boxes += detect_signatures(work)

            if ocr.get("words"):
                import re
                def norm(s: str) -> str:
                    return re.sub(r"\W+", "", s or "").lower()

                target = {norm(m["value"]) for m in pii_items}
                for w in ocr["words"]:
                    if norm(w["text"]) in target:
                        x, y, wdt, hgt = w["bbox"]
                        boxes.append([int(x), int(y), int(wdt), int(hgt)])

        # 6) Redact (skip for PDFs)
        if work.suffix.lower() != ".pdf":
            out_path = OUTPUT_DIR / f"{work.stem}_redacted.png"
            redact(work, boxes, out_path)
            output_uri = static_url(out_path)
        else:
            out_path = saved
            output_uri = static_url(saved)

        return {
            "filename": file.filename,
            "stored_path": str(saved),
            "output_path": str(out_path),
            "output_url": output_uri,
            "policy": policy,
            "ocr_chars": len(ocr.get("text", "")),
            "pii_detected": pii_items,
            "boxes_applied": boxes,
            "is_pdf": work.suffix.lower() == ".pdf",
        }

if __name__ == "__main__":
    print("MediTrustPipeline is a library; start the API with: uvicorn app.main:app --reload")
