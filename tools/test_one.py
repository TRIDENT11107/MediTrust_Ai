# run with: .venv_new\Scripts\python.exe tools\test_one.py Dataset/images/val/X_019.jpeg
import sys
from pathlib import Path
try:
    from ultralytics import YOLO
except Exception as e:
    print('Install ultralytics in your venv:', e); sys.exit(1)
weights = Path('runs/last.pt')
if not weights.exists():
    print('No runs/last.pt found. Copy your checkpoint to runs/last.pt or set weights path.')
    sys.exit(2)
model = YOLO(str(weights))
img = sys.argv[1]
results = model.predict(source=img, imgsz=640, device='cpu', conf=0.25, verbose=False)
r = results[0]
try:
    boxes = getattr(r, 'boxes')
    xyxy = getattr(boxes, 'xyxy', None)
    if xyxy is not None:
        print('Boxes (xyxy):', xyxy.tolist())
    else:
        print('Boxes object:', boxes)
except Exception as e:
    print('Could not parse results:', e)