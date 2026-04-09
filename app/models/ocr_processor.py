# app/models/ocr_processor.py
from pathlib import Path
from typing import Dict, Any, List

def run_ocr(image_path: Path) -> Dict[str, Any]:
    """
    Return {"text": str, "words": [{"text": str, "bbox": [x,y,w,h]}]}.
    Works even if pytesseract is not installed (returns empty).
    """
    text: str = ""
    words: List[Dict[str, Any]] = []

    try:
        from PIL import Image
        import pytesseract
        from pytesseract import Output

        img = Image.open(image_path).convert("RGB")
        text = pytesseract.image_to_string(img)

        data = pytesseract.image_to_data(img, output_type=Output.DICT)
        n = len(data["text"])
        for i in range(n):
            t = (data["text"][i] or "").strip()
            if not t:
                continue
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            words.append({"text": t, "bbox": [int(x), int(y), int(w), int(h)]})
    except Exception:
        # OCR optional; ignore any errors to keep pipeline robust
        pass

    return {"text": text, "words": words}
