# app/utils/file_handler.py
import re
import shutil
from pathlib import Path
from typing import Union
from fastapi import UploadFile

from app.core.config import (
    STATIC_DIR, STATIC_URL_PREFIX,
    UPLOADS_DIR, WORK_DIR, IMAGE_EXTS
)

def _sanitize_filename(name: str) -> str:
    name = name.strip().replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return name or "upload.bin"

async def save_upload(file: UploadFile) -> Path:
    """
    Persist the uploaded file to /static/uploads and return the saved Path.
    """
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    dest = UPLOADS_DIR / _sanitize_filename(file.filename or "upload.bin")
    with dest.open("wb") as f:
        f.write(await file.read())
    return dest

def ensure_image(saved_path: Path) -> Path:
    """
    If the upload is an image, copy/convert it to RGB PNG in /static/work and return that path.
    If it's a PDF, just return the original path (pipeline skips image-only steps for PDFs).
    """
    suffix = saved_path.suffix.lower()
    if suffix == ".pdf":
        return saved_path

    # Non-image types are just returned as-is
    if suffix not in IMAGE_EXTS:
        return saved_path

    try:
        from PIL import Image
        img = Image.open(saved_path).convert("RGB")
        WORK_DIR.mkdir(parents=True, exist_ok=True)
        out = WORK_DIR / f"{saved_path.stem}.png"
        img.save(out)
        return out
    except Exception:
        # Fallback: just copy the upload to work/
        WORK_DIR.mkdir(parents=True, exist_ok=True)
        out = WORK_DIR / saved_path.name
        try:
            shutil.copyfile(saved_path, out)
            return out
        except Exception:
            return saved_path

def static_url(path: Union[str, Path]) -> str:
    """
    Build a /static URL for a file under STATIC_DIR.
    """
    p = Path(path).resolve()
    base = STATIC_DIR.resolve()
    rel = p.relative_to(base)
    return f"{STATIC_URL_PREFIX}/{rel.as_posix()}"
