#!/usr/bin/env python3
"""
tools/ckpt_info.py

Quick inspector for PyTorch/Ultralytics checkpoint files (.pt).
It prints the top-level keys and common metadata like 'epoch' or 'best_fitness'.

Usage:
  .venv_new\Scripts\python.exe tools\ckpt_info.py --weights "C:\path\to\last.pt"
"""
import argparse
import torch
from pathlib import Path

def inspect_ckpt(path: Path):
    print('Loading checkpoint:', path)
    ckpt = torch.load(str(path), map_location='cpu')
    print('\nTop-level keys:')
    for k in sorted(ckpt.keys()):
        v = ckpt[k]
        print(f' - {k}: {type(v).__name__}')

    # Common metadata
    if 'epoch' in ckpt:
        print('\nFound epoch:', ckpt['epoch'])
    if 'best_fitness' in ckpt:
        print('Found best_fitness:', ckpt['best_fitness'])
    if 'best_map' in ckpt:
        print('Found best_map:', ckpt['best_map'])
    # Ultralytics sometimes stores 'model' key containing state_dict
    if 'model' in ckpt:
        try:
            sd = ckpt['model']
            if isinstance(sd, dict):
                print('Model state_dict keys sample:', list(sd.keys())[:5])
        except Exception:
            pass

    # If it's a simple state_dict (no metadata)
    if not any(k in ckpt for k in ('epoch','best_fitness','model')):
        print('\nNo common metadata fields found; this may be a plain state_dict.')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--weights', '-w', required=True, help='Path to checkpoint .pt')
    args = p.parse_args()
    path = Path(args.weights)
    if not path.exists():
        print('File not found:', path)
        return
    inspect_ckpt(path)

if __name__ == '__main__':
    main()
