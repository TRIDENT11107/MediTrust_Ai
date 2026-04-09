from pathlib import Path
from shutil import copy2
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATASET = ROOT / "Dataset"
IMAGES_SRC = DATASET / "images"

# ---------- helpers to locate files ----------
def find_table(names=("train","test")):
    out = {}
    for base in names:
        for ext in (".xlsx",".xls",".csv",".tsv"):
            p = DATASET / f"{base}{ext}"
            if p.exists():
                out[base] = p
                break
    return out

FILES = find_table(("train","test"))
if "train" not in FILES or "test" not in FILES:
    raise FileNotFoundError("Place train/test as .xlsx or .csv under Dataset/. Found: {}".format(FILES))

def load_df(p: Path) -> pd.DataFrame:
    return pd.read_excel(p) if p.suffix.lower() in (".xlsx",".xls") else pd.read_csv(p)

def lower_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={c: c.lower() for c in df.columns})

# ---------- class name/id mapping (optional) ----------
name_to_id = {}
id_to_name = {}
# categories.xlsx with columns like {id,name} or labelmap.txt lines "0 signature"
cats_xlsx = DATASET / "categories.xlsx"
cats_csv  = DATASET / "categories.csv"
lbl_txt   = DATASET / "labelmap.txt"
if cats_xlsx.exists() or cats_csv.exists():
    cpath = cats_xlsx if cats_xlsx.exists() else cats_csv
    dfc = load_df(cpath)
    dfc = lower_cols(dfc)
    id_col = next((c for c in dfc.columns if c in ("id","class_id","category_id")), None)
    name_col = next((c for c in dfc.columns if c in ("name","class_name","label")), None)
    if id_col and name_col:
        for _, r in dfc.iterrows():
            cid = int(r[id_col])
            cname = str(r[name_col]).strip()
            id_to_name[cid] = cname
            name_to_id[cname] = cid
elif lbl_txt.exists():
    for line in lbl_txt.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.replace(",", " ").split()
        try:
            cid = int(parts)
            cname = " ".join(parts[1:]) if len(parts) > 1 else str(cid)
            id_to_name[cid] = cname
            name_to_id[cname] = cid
        except Exception:
            continue

# ---------- target YOLO layout ----------
OUT_IMG_TRAIN = DATASET / "images" / "train"
OUT_IMG_VAL   = DATASET / "images" / "val"
OUT_LBL_TRAIN = DATASET / "labels" / "train"
OUT_LBL_VAL   = DATASET / "labels" / "val"
for p in (OUT_IMG_TRAIN, OUT_IMG_VAL, OUT_LBL_TRAIN, OUT_LBL_VAL):
    p.mkdir(parents=True, exist_ok=True)

# ---------- column resolver ----------
def pick(df_cols, candidates):
    for c in candidates:
        if c in df_cols:
            return c
    return None

def resolve_schema(df):
    cols = set(df.columns)
    # file name
    file_col = pick(cols, ["file_name","filename","image","image_name","img","path","image_path"])
    if not file_col:
        raise ValueError(f"Missing image filename column in {cols}")

    # category id or name
    cat_col = pick(cols, ["category_id","class_id","class","category","label","category_name","class_name"])
    if not cat_col:
        raise ValueError("Missing category column (category_id/class/label)")

    # normalized center format
    norm = {"x_center","y_center","width","height"}
    if norm.issubset(cols):
        return {"format":"center",
                "file":file_col, "cat":cat_col,
                "xc":"x_center","yc":"y_center","w":"width","h":"height"}

    # absolute min/max
    abs_mm = {"xmin","ymin","xmax","ymax"}
    if abs_mm.issubset(cols):
        return {"format":"xyxy",
                "file":file_col,"cat":cat_col,
                "xmin":"xmin","ymin":"ymin","xmax":"xmax","ymax":"ymax"}

    # top-left + size
    tlwh_sets = [
        ("left","top","width","height"),
        ("x","y","width","height"),
        ("x_min","y_min","w","h"),
        ("x1","y1","w","h"),
    ]
    for tl, tp, w, h in tlwh_sets:
        if {tl,tp,w,h}.issubset(cols):
            return {"format":"tlwh",
                    "file":file_col,"cat":cat_col,
                    "x":tl,"y":tp,"w":w,"h":h}

    raise ValueError("Could not detect bbox columns; expected one of: "
                     "(x_center,y_center,width,height) or (xmin,ymin,xmax,ymax) or (left,top,width,height).")

# ---------- image size helper ----------
def image_size(p: Path):
    try:
        from PIL import Image
        with Image.open(p) as im:
            return im.size  # (W,H)
    except Exception:
        return None, None

def copy_image(src: Path, dst_dir: Path) -> Path:
    dst = dst_dir / src.name
    if src.resolve() != dst.resolve():
        copy2(src, dst)
    return dst

# ---------- write a split ----------
def write_split(df_raw: pd.DataFrame, split: str):
    out_img = OUT_IMG_TRAIN if split == "train" else OUT_IMG_VAL
    out_lbl = OUT_LBL_TRAIN if split == "train" else OUT_LBL_VAL

    df = lower_cols(df_raw)
    schema = resolve_schema(set(df.columns))

    # group rows by image
    by_img = {}
    for _, r in df.iterrows():
        fn = str(r[schema["file"]])
        by_img.setdefault(fn, []).append(r)

    # whether category is string names
    cat_is_str = df[schema["cat"]].dtype == object

    for fn, rows in by_img.items():
        src = IMAGES_SRC / fn
        if not src.exists():
            src = IMAGES_SRC / Path(fn).name
        if not src.exists():
            print(f"[warn] missing image: {src}")
            continue

        dst = copy_image(src, out_img)
        W, H = image_size(src)
        if not W or not H:
            raise RuntimeError(f"Cannot read image size for {src}")

        with open(out_lbl / (dst.stem + ".txt"), "w", encoding="utf-8") as f:
            for r in rows:
                # category as id or name
                cid = r[schema["cat"]]
                if cat_is_str:
                    cname = str(cid).strip()
                    if cname not in name_to_id:
                        raise ValueError(f"Unknown class name '{cname}'. "
                                         f"Add it to categories.xlsx/labelmap.txt")
                    cid = name_to_id[cname]
                else:
                    cid = int(cid)
                    # convert 1-based to 0-based if needed
                    if df[schema["cat"]].min() == 1:
                        cid -= 1

                fmt = schema["format"]
                if fmt == "center":
                    xc = float(r[schema["xc"]]); yc = float(r[schema["yc"]])
                    w  = float(r[schema["w"]]);  h  = float(r[schema["h"]])
                elif fmt == "xyxy":
                    xmin = float(r[schema["xmin"]]); ymin = float(r[schema["ymin"]])
                    xmax = float(r[schema["xmax"]]); ymax = float(r[schema["ymax"]])
                    w  = (xmax - xmin) / W
                    h  = (ymax - ymin) / H
                    xc = (xmin + xmax) / 2 / W
                    yc = (ymin + ymax) / 2 / H
                elif fmt == "tlwh":
                    x0 = float(r[schema["x"]]); y0 = float(r[schema["y"]])
                    ww = float(r[schema["w"]]); hh = float(r[schema["h"]])
                    w  = ww / W
                    h  = hh / H
                    xc = (x0 + ww/2) / W
                    yc = (y0 + hh/2) / H
                else:
                    raise RuntimeError("Unknown format")

                # clamp and write
                xc = max(0.0, min(1.0, xc))
                yc = max(0.0, min(1.0, yc))
                w  = max(0.0, min(1.0, w))
                h  = max(0.0, min(1.0, h))
                f.write(f"{cid} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")

# ---------- run ----------
df_train = load_df(FILES["train"])
df_val   = load_df(FILES["test"])
write_split(df_train, "train")
write_split(df_val,   "val")
print("Done: labels in Dataset/labels/{train,val}, images in Dataset/images/{train,val}")
