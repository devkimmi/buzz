from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import transform

app = FastAPI(title="Sheet Music Transformer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transform.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
