# app/models/redaction_engine.py
from pathlib import Path
from typing import List

def redact(image_path: Path, boxes: List[List[int]], out_path: Path) -> None:
    """
    Draw opaque black rectangles over [x, y, w, h] boxes and save to out_path.
    """
    from PIL import Image, ImageDraw

    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    for x, y, w, h in boxes or []:
        draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
