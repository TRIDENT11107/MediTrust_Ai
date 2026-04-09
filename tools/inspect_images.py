from pathlib import Path
from pprint import pprint
paths = [Path('static/uploads/tr_1.png'), Path('static/work/tr_1.png'), Path('static/uploads/tr_2.png'), Path('static/work/tr_2.png')]

def try_pil(p: Path):
    try:
        from PIL import Image
        im = Image.open(p)
        im.verify()
        im = Image.open(p)
        return {'format': im.format, 'mode': im.mode, 'size': im.size}
    except Exception as e:
        return {'error': repr(e)}

def try_cv2(p: Path):
    try:
        import cv2
        arr = cv2.imread(str(p))
        if arr is None:
            return {'error': 'cv2.imread returned None'}
        return {'shape': arr.shape}
    except Exception as e:
        return {'error': repr(e)}

def main():
    for p in paths:
        print('---')
        print('Path:', p)
        print('Exists:', p.exists())
        if not p.exists():
            continue
        print('Size:', p.stat().st_size)
        print('PIL:', try_pil(p))
        print('cv2:', try_cv2(p))

    # If uploads are fine and work files broken, rewrite work files from uploads using cv2
    up1 = Path('static/uploads/tr_1.png')
    wk1 = Path('static/work/tr_1.png')
    if up1.exists() and (not wk1.exists() or try_pil(wk1).get('error')):
        try:
            import cv2
            img = cv2.imread(str(up1))
            cv2.imwrite(str(wk1), img)
            print('Rewrote', wk1)
        except Exception as e:
            print('Failed to rewrite', wk1, e)

    up2 = Path('static/uploads/tr_2.png')
    wk2 = Path('static/work/tr_2.png')
    if up2.exists() and (not wk2.exists() or try_pil(wk2).get('error')):
        try:
            import cv2
            img = cv2.imread(str(up2))
            cv2.imwrite(str(wk2), img)
            print('Rewrote', wk2)
        except Exception as e:
            print('Failed to rewrite', wk2, e)

if __name__ == '__main__':
    main()
