#!/usr/bin/env python3
r"""
Quick integrity + inference check for YOLO ultralytics checkpoints.

This script will:
- find the most recent `last.pt` under `C:\Users\rasto\runs` or `./runs` (project)
- try to load it via `ultralytics.YOLO`
- run inference on up to N images from `Dataset/images/val` and report detection counts

Usage (from repo root):
  .venv_new\Scripts\python.exe tools\quick_check.py --weights <path> --samples 5 --device cpu

If `--weights` is not provided, the script attempts to auto-discover the newest `last.pt`.
"""

import argparse
import os
import sys
from pathlib import Path

def find_latest_last_pt():
    candidates = []
    base = Path(r"C:\Users\rasto\runs")
    if base.exists():
        for p in base.rglob('last.pt'):
            candidates.append(p)
    proj_runs = Path.cwd() / 'runs'
    if proj_runs.exists():
        for p in proj_runs.rglob('last.pt'):
            candidates.append(p)
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return str(candidates[0])

def get_val_images(n):
    p = Path.cwd() / 'Dataset' / 'images' / 'val'
    if not p.exists():
        return []
    imgs = [str(p / f) for f in sorted(os.listdir(p)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return imgs[:n]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', '-w', help='Path to weights (last.pt). If omitted auto-discover', default=None)
    parser.add_argument('--samples', '-n', type=int, default=5, help='Number of val images to run inference on')
    parser.add_argument('--device', '-d', default='cpu', help='Device to run inference on (cpu or cuda)')
    args = parser.parse_args()

    weights = args.weights or find_latest_last_pt()
    if not weights:
        print('No checkpoint found. Provide --weights or copy last.pt into runs/last.pt')
        sys.exit(2)

    print('Using checkpoint:', weights)
    try:
        from ultralytics import YOLO
    except Exception as e:
        print('ultralytics not importable:', e)
        print('Activate your venv and install ultralytics, or run: .venv_new\\Scripts\\python.exe -m pip install ultralytics')
        sys.exit(1)

    try:
        model = YOLO(weights)
    except Exception as e:
        print('Failed to load model:', e)
        sys.exit(1)
    imgs = get_val_images(args.samples)
    if not imgs:
        print('No val images found at Dataset/images/val — quick inference cannot be run.')
        sys.exit(1)

    print('Running quick inference on', len(imgs), 'images using device=', args.device)
    for img in imgs:
        print('\n--> Predicting', img)
        try:
            results = model.predict(source=img, imgsz=640, device=args.device, conf=0.25, verbose=False)
            # results may be a list-like
            if not results:
                print('  No results returned')
                continue
            r = results[0]
            # Try to extract boxes length in a few ways
            det_count = None
            try:
                # ultralytics Results has .boxes
                det_count = len(getattr(r, 'boxes', []))
            except Exception:
                det_count = None
            if det_count is None:
                try:
                    # fallback: numpy array of boxes
                    b = getattr(r, 'boxes', None)
                    det_count = len(b) if b is not None else 'unknown'
                except Exception:
                    det_count = 'unknown'
            print('  Detections:', det_count)
        except Exception as e:
            print('  Prediction failed:', e)

    print('\nQuick check finished. If model loaded and predictions ran, checkpoint appears usable.')

if __name__ == '__main__':
    main()
