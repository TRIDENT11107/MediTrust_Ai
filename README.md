# MediTrust AI

FastAPI backend with /ping, /upload, and extra routes under /api/v1.  
Static outputs are served from /static (storage/).  

## Run with Docker
docker compose up --build

- API: http://localhost:3000  
- Docs: http://localhost:3000/docs  
- Test: POST /upload with header `x-api-key: dev-key` and one or more files.

## Run locally (Windows 3.11)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000

## Optional UI
npm install
npm start        # http://localhost:5173

## Endpoints
- GET /ping → health  
- POST /upload → accepts multipart form field `files` (one or many), optional `policy` (default `research_share`)

## Outputs
- Redacted images saved to storage/outputs and reachable via /static/outputs/<file>.png.
