import asyncio
import sys
from pathlib import Path

# Ensure repo root is on sys.path so 'app' package can be imported when running this script
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.pipeline import MediTrustPipeline

SAMPLE = Path('Dataset/images/val/X_019.jpeg')

async def main():
    if not SAMPLE.exists():
        print('Sample not found:', SAMPLE)
        return
    pipeline = MediTrustPipeline()
    # Create a minimal UploadFile-like object that the pipeline expects
    class DummyUpload:
        def __init__(self, path: Path):
            self.path = path
            self.filename = path.name
        async def read(self):
            return self.path.read_bytes()

    dummy = DummyUpload(SAMPLE)
    res = await pipeline.process_document(dummy, policy='default')
    print(res)

if __name__ == '__main__':
    asyncio.run(main())
