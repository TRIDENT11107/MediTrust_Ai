from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import router as api_router
from app.core.config import FRONTEND_DIR, STATIC_DIR, STATIC_URL_PREFIX

app = FastAPI(title="MediTrust AI", version="0.1.0")

# Enable CORS for frontend dev servers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static API assets first, then API routes, then the frontend catch-all.
app.mount(STATIC_URL_PREFIX, StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=3000, reload=True)
