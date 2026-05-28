from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings
from app.core.qdrant_client import get_qdrant_client, ensure_collection_exists

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting AI Avatar API")
    print(f"Qdrant: {settings.qdrant_host}:{settings.qdrant_port}")
    print(f"Ollama: {settings.ollama_host}")
    print(f"Model: {settings.ollama_model}")

    qdrant = get_qdrant_client()
    ensure_collection_exists(qdrant)

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
    qdrant = get_qdrant_client()

    try:
        collections = [c.name for c in qdrant.get_collections().collections]
        qdrant_ok = settings.qdrant_collection_name in collections
    except Exception as e:
        return {
            "status": "degraded",
            "qdrant": f"error: {str(e)}",
        }

    return {
        "status": "ok",
        "version": "0.1.0",
        "qdrant": "ok" if qdrant_ok else "collection missing",
        "collection": settings.qdrant_collection_name,
    }

@app.get("/")
async def root():
    return {"message": "AI Avatar API is running"}