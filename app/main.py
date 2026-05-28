from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings
from app.core.qdrant_client import get_qdrant_client, ensure_collection_exists
from app.core.ollama_client import get_ollama_client, verify_ollama_models

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting AI Avatar API")
    print(f"Qdrant: {settings.qdrant_host}:{settings.qdrant_port}")
    print(f"Ollama: {settings.ollama_host}")
    print(f"Model: {settings.ollama_model}")

    qdrant = get_qdrant_client()
    ensure_collection_exists(qdrant)

    ollama = get_ollama_client()
    verify_ollama_models(ollama)

    yield

    ollama.close()
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
    ollama = get_ollama_client()

    try:
        collections = [c.name for c in qdrant.get_collections().collections]
        qdrant_status = (
            "ok" if settings.qdrant_collection_name in collections
            else "collection missing"
        )
    except Exception as e:
        qdrant_status = f"error: {e}"
    
    try:
        response = ollama.get("/api/tags")
        models = [m["name"] for m in response.json().get("models", [])]
        ollama_status = "ok" if models else "no models"
    except Exception as e:
        ollama_status = f"error: {e}"

    overall = (
        "ok" if qdrant_status == "ok" and ollama_status == "ok"
        else "degraded"
    )

    return {
        "status": overall,
        "version": "0.1.0",
        "services": {
            "qdrant": qdrant_status,
            "ollama": ollama_status,
        },
        "collection": settings.qdrant_collection_name,
    }

@app.get("/")
async def root():
    return {"message": "AI Avatar API is running"}