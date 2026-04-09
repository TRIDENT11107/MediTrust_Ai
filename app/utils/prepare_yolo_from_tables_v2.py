# app/utils/prepare_yolo_from_tables_v2.py
from pathlib import Path
from shutil import copy2
import pandas as pd
import ast

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "Dataset"
IMAGES_SRC = DATASET / "images"

def pick_table(basename: str):
    # Prefer .csv then .xlsx/.xls; case-insensitive
    for ext in (".csv", ".xlsx", ".xls"):
        for p in DATASET.glob(f"{basename}{ext}"):
            return p
        for p in DATASET.glob(f"{basename.upper()}{ext}"):
            return p
        for p in DATASET.glob(f"{basename.capitalize()}{ext}"):
            return p
    return None

train_tbl = pick_table("train")
test_tbl  = pick_table("test")
if not train_tbl or not test_tbl:
    raise FileNotFoundError(f"Could not find train/test tables next to {DATASET}. "
                            f"Expected train/test with .csv/.xlsx/.xls. Found: "
                            f"train={train_tbl}, test={test_tbl}")

# categories: id,name (1-based ids) -> map to 0-based and YAML names
cats = DATASET / "categories.csv"
name_map = {}
if cats.exists():
    dfc = pd.read_csv(cats)
    dfc.columns = [c.lower() for c in dfc.columns]
    for _, r in dfc.iterrows():
        name_map[int(r["id"]) - 1] = str(r["name"]).strip()

# image_ids.csv: height,width,id,file_name
sizes = {}
name_by_image_id = {}
img_ids = DATASET / "image_ids.csv"
if img_ids.exists():
    dfi = pd.read_csv(img_ids)
    dfi.columns = [c.lower() for c in dfi.columns]
    for _, r in dfi.iterrows():
        idx = int(r["id"])
        fn = str(r["file_name"])
        W = int(round(float(r["width"])))
        H = int(round(float(r["height"])))
        sizes[fn] = (W, H)
        name_by_image_id[idx] = fn

# Targets
OUT_IMG_TRAIN = DATASET / "images" / "train"
OUT_IMG_VAL   = DATASET / "images" / "val"
OUT_LBL_TRAIN = DATASET / "labels" / "train"
OUT_LBL_VAL   = DATASET / "labels" / "val"
for p in (OUT_IMG_TRAIN, OUT_IMG_VAL, OUT_LBL_TRAIN, OUT_LBL_VAL):
    p.mkdir(parents=True, exist_ok=True)

def load_table(p: Path) -> pd.DataFrame:
    return pd.read_excel(p) if p.suffix.lower() in (".xlsx", ".xls") else pd.read_csv(p)

def find_image(fn: str) -> Path | None:
    # try direct, then basename search under images/
    direct = IMAGES_SRC / fn
    if direct.exists():
        return direct
    for cand in IMAGES_SRC.rglob(Path(fn).name):
        if cand.is_file():
            return cand
    return None

def write_split(df: pd.DataFrame, split: str):
    out_img = OUT_IMG_TRAIN if split == "train" else OUT_IMG_VAL
    out_lbl = OUT_LBL_TRAIN if split == "train" else OUT_LBL_VAL
    df = df.rename(columns={c: c.lower() for c in df.columns})

    # Expected columns from your files:
    # area, bbox(str "[xc,yc,w,h]"), category_id (1..4), id, image_id
    needed = {"bbox", "category_id"}
    if not needed.issubset(set(df.columns)):
        raise ValueError(f"Missing required columns {needed} in {list(df.columns)}")

    # Resolve file_name by image_id using image_ids.csv
    if "file_name" not in df.columns:
        if "image_id" not in df.columns:
            raise ValueError("Need either file_name or image_id column")
        df["file_name"] = df["image_id"].map(name_by_image_id)

    by_img = {}
    for _, r in df.iterrows():
        fn = str(r["file_name"])
        by_img.setdefault(fn, []).append(r)

    for fn, rows in by_img.items():
        src = find_image(fn)
        if not src:
            print(f"[warn] missing image under Dataset/images: {fn}")
            continue

        # copy image
        dst = out_img / src.name
        if src.resolve() != dst.resolve():
            dst.parent.mkdir(parents=True, exist_ok=True)
            copy2(src, dst)

        # image size (many boxes are normalized already; keep fallback)
        W, H = sizes.get(fn, (None, None))
        if W is None or H is None:
            try:
                from PIL import Image
                with Image.open(src) as im:
                    W, H = im.size
            except Exception:
                pass

        # write label file
        lines = []
        for r in rows:
            # bbox string -> list of floats [xc, yc, w, h] already normalized
            b = r["bbox"]
            if isinstance(b, str):
                xc, yc, w, h = map(float, ast.literal_eval(b))
            else:
                xc, yc, w, h = map(float, b)

            cid = int(r["category_id"]) - 1  # 0-based for YOLO
            # clamp just in case
            xc = max(0.0, min(1.0, xc)); yc = max(0.0, min(1.0, yc))
            w  = max(0.0, min(1.0,  w));  h  = max(0.0, min(1.0,  h))
            lines.append(f"{cid} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")

        lbl = out_lbl / (dst.stem + ".txt")
        with open(lbl, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

# Run conversions
df_train = load_table(train_tbl)
df_val   = load_table(test_tbl)
write_split(df_train, "train")
write_split(df_val,   "val")

# Write a dataset YAML
yaml = DATASET / "meditrust.yaml"
names_yaml = "\n".join([f"  {i}: {name_map.get(i, n)}"
                        for i, n in enumerate(["signature","initials","redaction","date"])])
yaml.write_text(f"path: Dataset\ntrain: images/train\nval: images/val\nnames:\n{names_yaml}\n", encoding="utf-8")

print("OK: images/labels created and meditrust.yaml written in Dataset/")
