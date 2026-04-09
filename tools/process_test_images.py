import asyncio
import sys
from pathlib import Path
import random

# Ensure repo root on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.pipeline import MediTrustPipeline

TEST_DIR = ROOT / 'Dataset' / 'images' / 'test'

async def process_file(path: Path, pipeline: MediTrustPipeline):
    class DummyUpload:
        def __init__(self, path: Path):
            self.path = path
            self.filename = path.name
        async def read(self):
            return self.path.read_bytes()

    print('Processing', path)
    res = await pipeline.process_document(DummyUpload(path), policy='default')
    print('Result:')
    print(res)

async def main():
    if not TEST_DIR.exists():
        print('Test dir not found:', TEST_DIR)
        return
    imgs = [p for p in TEST_DIR.iterdir() if p.is_file()]
    if not imgs:
        print('No images in', TEST_DIR)
        return
    # pick two random images (or fewer if not enough)
    pick = random.sample(imgs, min(2, len(imgs)))
    pipeline = MediTrustPipeline()
    for p in pick:
        await process_file(p, pipeline)

if __name__ == '__main__':
    asyncio.run(main())
