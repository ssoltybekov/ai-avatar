from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting AI Avatar API")
    print(f"Qdrant: {settings.qdrant_host}:{settings.qdrant_port}")
    print(f"Ollama: {settings.ollama_host}")
    print(f"Model: {settings.ollama_model}")

    yield

    print("Shutting down AI Avatar API")

app = FastAPI(
    title="AI Avatar API",
    description="AI",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "version": "0.1.0"
    }

@app.get("/")
async def root():
    return {"message": "AI Avatar API is running"}