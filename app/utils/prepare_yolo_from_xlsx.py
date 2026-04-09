import csv
from pathlib import Path
import pandas as pd
from shutil import copy2

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "Dataset"
IMAGES_SRC = DATASET / "images"    # current master images
OUT_IMG_TRAIN = DATASET / "images" / "train"
OUT_IMG_VAL   = DATASET / "images" / "val"
OUT_LBL_TRAIN = DATASET / "labels" / "train"
OUT_LBL_VAL   = DATASET / "labels" / "val"

# edit these if your file names differ
TRAIN_FILE = DATASET / "train.xlsx"
VAL_FILE   = DATASET / "test.xlsx"
IMAGE_IDS  = DATASET / "image_ids.xlsx"   # optional size lookup

for p in [OUT_IMG_TRAIN, OUT_IMG_VAL, OUT_LBL_TRAIN, OUT_LBL_VAL]:
    p.mkdir(parents=True, exist_ok=True)

# Try to load image sizes if available
sizes = {}
if IMAGE_IDS.exists():
    df_sizes = pd.read_excel(IMAGE_IDS)
    # expected columns: file_name,width,height (edit if different)
    for _, r in df_sizes.iterrows():
        sizes[str(r["file_name"])] = (int(r["width"]), int(r["height"]))

def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    return pd.read_csv(path)

def write_split(df: pd.DataFrame, split: str):
    out_img = OUT_IMG_TRAIN if split == "train" else OUT_IMG_VAL
    out_lbl = OUT_LBL_TRAIN if split == "train" else OUT_LBL_VAL

    # Accept either normalized or absolute boxes. Expected columns:
    # file_name, x_center, y_center, width, height, category_id  (normalized 0..1)
    # OR: file_name, xmin, ymin, xmax, ymax, category_id         (absolute pixels)
    norm_cols = {"x_center","y_center","width","height"}
    abs_cols  = {"xmin","ymin","xmax","ymax"}
    has_norm = norm_cols.issubset({c.lower() for c in df.columns})
    has_abs  = abs_cols.issubset({c.lower() for c in df.columns})

    # normalize column names (lowercase)
    df = df.rename(columns={c: c.lower() for c in df.columns})

    by_image = {}
    for _, r in df.iterrows():
        fn = str(r["file_name"])
        by_image.setdefault(fn, []).append(r)

    for fn, rows in by_image.items():
        src = IMAGES_SRC / fn
        if not src.exists():
            # try without dirs: if fn has path parts
            src = IMAGES_SRC / Path(fn).name
        if not src.exists():
            print(f"WARNING: missing image {src}")
            continue
        dst = out_img / src.name
        if src.resolve() != dst.resolve():
            copy2(src, dst)

        W, H = sizes.get(fn, (None, None))
        if not has_norm and (W is None or H is None):
            from PIL import Image
            with Image.open(src) as im:
                W, H = im.size

        with open(out_lbl / (Path(fn).stem + ".txt"), "w", encoding="utf-8") as f:
            for r in rows:
                cls = int(r["category_id"])
                if has_norm:
                    xc, yc, w, h = float(r["x_center"]), float(r["y_center"]), float(r["width"]), float(r["height"])
                elif has_abs:
                    xmin, ymin, xmax, ymax = float(r["xmin"]), float(r["ymin"]), float(r["xmax"]), float(r["ymax"])
                    w  = (xmax - xmin) / W
                    h  = (ymax - ymin) / H
                    xc = (xmin + xmax) / 2 / W
                    yc = (ymin + ymax) / 2 / H
                else:
                    raise RuntimeError("Table must have either normalized (x_center,y_center,width,height) or absolute (xmin,ymin,xmax,ymax) columns")
                f.write(f"{cls} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")

df_train = load_table(TRAIN_FILE)
df_val   = load_table(VAL_FILE)
write_split(df_train, "train")
write_split(df_val,   "val")
print("Done: YOLO data written to Dataset/images/{train,val} and Dataset/labels/{train,val}")
