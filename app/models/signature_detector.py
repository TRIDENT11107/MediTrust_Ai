# app/models/signature_detector.py
from pathlib import Path
from typing import List, Optional

_MODEL = None


def _load_model(weights: Optional[str] = None):
    """Lazy-load an Ultralytics YOLO model.

    weights: path to a .pt weights file. If None the loader will attempt to use
    './runs/last.pt' which is the repository convention used by training tools.
    Returns the YOLO model instance or None if ultralytics is not available.
    """
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    try:
        from ultralytics import YOLO
    except Exception:
        # ultralytics not installed in this environment
        return None

    w = weights or (Path.cwd() / 'runs' / 'last.pt')
    if not Path(w).exists():
        # try repo root fallback (sometimes copied to project root)
        w2 = Path.cwd() / '..' / 'runs' / 'last.pt'
        if Path(w2).exists():
            w = w2
    try:
        model = YOLO(str(w))
        _MODEL = model
        return _MODEL
    except Exception:
        return None


def _boxes_from_result(res) -> List[List[int]]:
    """Convert ultralytics Results object to list of [x,y,w,h] ints.

    Uses a few fallbacks depending on the runtime version/structure.
    """
    boxes = []
    try:
        # ultralytics Results often expose `.boxes.xyxy` or `.boxes` list-like
        b = getattr(res, 'boxes', None)
        if b is None:
            return boxes
        # If b has `.xyxy` attribute (tensor/np), iterate
        xyxy = getattr(b, 'xyxy', None)
        if xyxy is not None:
            for row in xyxy.tolist():
                x1, y1, x2, y2 = map(int, row[:4])
                boxes.append([x1, y1, x2 - x1, y2 - y1])
            return boxes
        # Else, b may be an iterable of Box objects with .xyxy
        try:
            for box in b:
                coords = getattr(box, 'xyxy', None)
                if coords is None:
                    # box may be a simple array-like
                    arr = list(box)
                    if len(arr) >= 4:
                        x1, y1, x2, y2 = map(int, arr[:4])
                        boxes.append([x1, y1, x2 - x1, y2 - y1])
                else:
                    # coords may be a tensor/np array
                    vals = coords.tolist() if hasattr(coords, 'tolist') else list(coords)
                    x1, y1, x2, y2 = map(int, vals[:4])
                    boxes.append([x1, y1, x2 - x1, y2 - y1])
            return boxes
        except Exception:
            return boxes
    except Exception:
        return boxes


def detect_signatures(image_path: Path, weights: Optional[str] = None) -> List[List[int]]:
    """Run object detection on `image_path` and return list of [x,y,w,h] boxes.

    If the `ultralytics` package or weights are not available this will return an
    empty list so the rest of the pipeline can continue (OCR/PII redaction still works).
    """
    model = _load_model(weights)
    if model is None:
        return []

    try:
        results = model.predict(source=str(image_path), imgsz=640, device='cpu', conf=0.25, verbose=False)
        if not results:
            return []
        # Use first result
        res = results[0]
        return _boxes_from_result(res)
    except Exception:
        return []

