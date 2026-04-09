import requests
import sys
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8002
URL = f'http://127.0.0.1:{PORT}/api/process'
SAMPLE = Path('Dataset/images/val/X_081.jpeg')

def main():
    if not SAMPLE.exists():
        print('Sample not found:', SAMPLE)
        return
    with SAMPLE.open('rb') as fh:
        files = {'file': (SAMPLE.name, fh, 'image/jpeg')}
        print('Posting to', URL)
        r = requests.post(URL, files=files)
        print('Status:', r.status_code)
        try:
            print(r.json())
        except Exception:
            print(r.text)

if __name__ == '__main__':
    main()
