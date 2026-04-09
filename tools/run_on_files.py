import sys
from pathlib import Path

# Ensure repo root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.models.signature_detector import _load_model, detect_signatures

def main(paths):
    print('Repo root:', ROOT)
    model = _load_model()
    if model is None:
        print('Model not available (ultralytics or weights missing).')
    else:
        print('Model loaded:', type(model))

    for p in paths:
        path = Path(p)
        print('\n---')
        print('File:', path)
        if not path.exists():
            print('  NOT FOUND')
            continue
        boxes = detect_signatures(path)
        print('  Boxes:', boxes)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: run_on_files.py <path1> [<path2> ...]')
        sys.exit(1)
    main(sys.argv[1:])
