"""
Sync images with label files and optionally create a test split.

Usage examples (run from project root):
  python tools\sync_images_with_labels.py --dataset Dataset --dry-run
  python tools\sync_images_with_labels.py --dataset Dataset --create-test 0.1
  python tools\sync_images_with_labels.py --dataset Dataset --move --create-test 0.05

What it does:
- Reads label files under `Dataset/labels/train` and `Dataset/labels/val`.
- Copies matching images from `Dataset/images/` (top-level) into
  `Dataset/images/train` and `Dataset/images/val` respectively.
- If `--create-test FRACTION` is provided it will pick that fraction
  of images from the training set, move them to `Dataset/images/test`
  and move their label files from `Dataset/labels/train` to
  `Dataset/labels/test` (so they are reserved for testing).

Notes:
- The script looks for files with common image extensions and will
  match by stem (filename without extension). It is safe by default
  because it performs a dry-run unless `--move` is passed.
"""

from pathlib import Path
import shutil
import argparse
import random
import sys

IMG_EXTS = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']


def find_image(images_dir: Path, stem: str):
    # Search for an image with the given stem in images_dir (non-recursive)
    for ext in IMG_EXTS:
        candidate = images_dir / (stem + ext)
        if candidate.exists():
            return candidate
    # try case-insensitive / any extension
    for p in images_dir.iterdir():
        if not p.is_file():
            continue
        if p.stem == stem:
            return p
    return None


def sync_split(images_dir: Path, labels_dir: Path, out_images_dir: Path, dry_run=True, move=False):
    out_images_dir.mkdir(parents=True, exist_ok=True)
    label_files = sorted([p for p in labels_dir.glob('*.txt') if p.is_file()])
    copied = 0
    missing = []
    for lbl in label_files:
        stem = lbl.stem
        src = find_image(images_dir, stem)
        if not src:
            missing.append(stem)
            continue
        dst = out_images_dir / src.name
        if src.resolve() == dst.resolve():
            # already in place
            copied += 1
            continue
        if dry_run:
            print(f"DRY-RUN: would copy {src} -> {dst}")
        else:
            if move:
                print(f"Moving {src} -> {dst}")
                shutil.move(str(src), str(dst))
            else:
                print(f"Copying {src} -> {dst}")
                shutil.copy2(str(src), str(dst))
        copied += 1

    return copied, missing


def create_test_split(dataset: Path, fraction: float, dry_run=True):
    # Move a fraction of training items into images/test and labels/test
    img_train = dataset / 'images' / 'train'
    lbl_train = dataset / 'labels' / 'train'
    img_test = dataset / 'images' / 'test'
    lbl_test = dataset / 'labels' / 'test'
    img_test.mkdir(parents=True, exist_ok=True)
    lbl_test.mkdir(parents=True, exist_ok=True)

    # list label basenames in train
    train_labels = [p for p in lbl_train.glob('*.txt') if p.is_file()]
    n = len(train_labels)
    if n == 0:
        print('No training labels found to sample for test split.')
        return 0
    k = max(1, int(n * fraction))
    selected = random.sample(train_labels, k)
    moved = 0
    for lbl in selected:
        stem = lbl.stem
        # corresponding image
        img = find_image(img_train, stem)
        if not img:
            # try top-level images as fallback
            img = find_image(dataset / 'images', stem)
        if not img:
            print(f"WARNING: test selection missing image for {stem}")
            continue
        dst_img = img_test / img.name
        dst_lbl = lbl_test / lbl.name
        if dry_run:
            print(f"DRY-RUN: would move {img} -> {dst_img}")
            print(f"DRY-RUN: would move {lbl} -> {dst_lbl}")
        else:
            print(f"Moving image {img} -> {dst_img}")
            shutil.move(str(img), str(dst_img))
            print(f"Moving label {lbl} -> {dst_lbl}")
            shutil.move(str(lbl), str(dst_lbl))
        moved += 1
    return moved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='Dataset', help='Path to dataset directory (default: Dataset)')
    parser.add_argument('--dry-run', action='store_true', help='Print actions without copying/moving')
    parser.add_argument('--move', action='store_true', help='Move files instead of copying (destructive)')
    parser.add_argument('--create-test', type=float, default=0.0, help='Create a test split by moving this fraction of training items to test (0..1)')
    args = parser.parse_args()

    dataset = Path(args.dataset)
    imgs = dataset / 'images'
    lbls = dataset / 'labels'

    if not dataset.exists():
        print(f"Dataset path {dataset} does not exist", file=sys.stderr)
        sys.exit(2)

    # Train
    train_lbl_dir = lbls / 'train'
    val_lbl_dir = lbls / 'val'
    if not train_lbl_dir.exists() and not val_lbl_dir.exists():
        print('No labels/train or labels/val directories found - nothing to do')
        sys.exit(0)

    copied_train, missing_train = sync_split(imgs, train_lbl_dir, imgs / 'train', dry_run=args.dry_run, move=args.move)
    copied_val, missing_val = sync_split(imgs, val_lbl_dir, imgs / 'val', dry_run=args.dry_run, move=args.move)

    print(f"Train images processed: {copied_train}, missing images for {len(missing_train)} labels")
    if missing_train:
        print('Missing train images (examples):', missing_train[:10])
    print(f"Val images processed: {copied_val}, missing images for {len(missing_val)} labels")

    if args.create_test and args.create_test > 0.0:
        moved = create_test_split(dataset, args.create_test, dry_run=args.dry_run)
        print(f"Test items moved: {moved}")

    print('Done.')


if __name__ == '__main__':
    main()
