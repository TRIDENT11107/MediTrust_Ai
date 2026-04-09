import asyncio
import sys
from pathlib import Path

# Ensure repo root is on sys.path so 'app' package can be imported
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.pipeline import MediTrustPipeline

FILES = [Path('static/uploads/tr_1.png'), Path('static/uploads/tr_2.png')]

async def process(path: Path):
    if not path.exists():
        print('Not found:', path)
        return

    pipeline = MediTrustPipeline()

    class DummyUpload:
        def __init__(self, path: Path):
            self.path = path
            self.filename = path.name
        async def read(self):
            return self.path.read_bytes()

    dummy = DummyUpload(path)
    res = await pipeline.process_document(dummy, policy='default')
    print('\n---')
    print('File:', path)
    print('Output JSON:')
    print(res)

async def main():
    for p in FILES:
        await process(p)

if __name__ == '__main__':
    asyncio.run(main())
