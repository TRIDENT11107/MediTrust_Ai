# MediTrust AI Frontend

This folder contains the optional React + Vite frontend for MediTrust AI.

## Frontend

```bash
cd meditrust-ai-react
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

## Backend

Run the FastAPI backend from the project root:

```bash
python -m pip install -r ../requirements.txt
uvicorn app.main:app --reload --port 3000
```

The frontend expects:
- `GET http://localhost:3000/api/health`
- `POST http://localhost:3000/api/process`

`POST /api/process` accepts multipart form data with field name `file`.
