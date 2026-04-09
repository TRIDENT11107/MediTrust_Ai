# app/core/config.py
from pathlib import Path

# Project root: .../MediTrust_Ai
ROOT_DIR = Path(__file__).resolve().parents[2]

# Static dir served at /static
STATIC_DIR = ROOT_DIR / "static"
UPLOADS_DIR = STATIC_DIR / "uploads"
WORK_DIR = STATIC_DIR / "work"
OUTPUT_DIR = STATIC_DIR / "outputs"

# URL prefix used by FastAPI mount
STATIC_URL_PREFIX = "/static"

# Ensure directories exist
for p in (STATIC_DIR, UPLOADS_DIR, WORK_DIR, OUTPUT_DIR):
    p.mkdir(parents=True, exist_ok=True)

# Allowed image types
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp", ".gif"}

# Prefer the built React frontend. Fall back to the legacy static frontend if the
# build output is not available yet.
REACT_FRONTEND_DIR = ROOT_DIR / "meditrust-ai-react" / "dist"
LEGACY_FRONTEND_DIR = ROOT_DIR / "Frontend"
FRONTEND_DIR = REACT_FRONTEND_DIR if REACT_FRONTEND_DIR.exists() else LEGACY_FRONTEND_DIR

__all__ = [
    "ROOT_DIR",
    "STATIC_DIR",
    "UPLOADS_DIR",
    "WORK_DIR",
    "OUTPUT_DIR",
    "STATIC_URL_PREFIX",
    "IMAGE_EXTS",
    "REACT_FRONTEND_DIR",
    "LEGACY_FRONTEND_DIR",
    "FRONTEND_DIR",
]
