import asyncio
from pathlib import Path
import sys

# Ensure repo root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.pipeline import MediTrustPipeline

P = Path('static/uploads/tr_2.png')

class DummyUpload:
    def __init__(self, path: Path):
        self.path = path
        self.filename = path.name
    async def read(self):
        return self.path.read_bytes()

async def main():
    if not P.exists():
        print('File not found:', P)
        return
    pipeline = MediTrustPipeline()
    res = await pipeline.process_document(DummyUpload(P), policy='default')
    print(res)

if __name__ == '__main__':
    asyncio.run(main())
