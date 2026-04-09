from pathlib import Path
import sys

# Ensure repo root is on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.models.signature_detector import _load_model, detect_signatures

SAMPLES = [Path('Dataset/images/val/X_019.jpeg'), Path('Dataset/images/val/X_081.jpeg')]

def main():
    print('Repo root:', ROOT)
    model = _load_model()
    if model is None:
        print('Ultralytics YOLO model not available or weights missing. Signature detection will be skipped.')
    else:
        print('Model loaded:', type(model))

    for s in SAMPLES:
        print('\nSample:', s)
        if not s.exists():
            print('  File not found')
            continue
        boxes = detect_signatures(s)
        print('  Detected boxes:', boxes)

if __name__ == '__main__':
    main()
