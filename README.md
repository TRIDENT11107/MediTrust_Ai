# MediTrust AI

FastAPI backend with a React frontend in `meditrust-ai-react/`.

## Main frontend

- Source: `meditrust-ai-react/`
- Built assets: `meditrust-ai-react/dist/`
- Legacy static prototype: `Frontend/`

The backend prefers serving the built React app from `meditrust-ai-react/dist`. If that build is missing, it falls back to the legacy static frontend.

## Backend

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

Backend endpoints:
- `GET /api/health`
- `POST /api/process`
- `/static/...` for uploaded files and generated outputs

## React frontend

Development:

```powershell
npm run dev:frontend
```

Production build:

```powershell
npm run build:frontend
```

Then either:
- open the backend at `http://localhost:3000`, or
- serve the built frontend with `npm start` on `http://localhost:5173`

## Outputs

- Generated files are written under `static/outputs`
- API responses include `output_url`, for example `/static/outputs/<file>`
