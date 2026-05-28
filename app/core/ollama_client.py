from functools import lru_cache
import httpx
from app.config import get_settings

settings = get_settings()

@lru_cache
def get_ollama_client() -> httpx.Client:
    client = httpx.Client(
        base_url=settings.ollama_host,
        timeout=httpx.Timeout(
            connect=10.0,    
            read=120.0,      
            write=10.0,      
            pool=10.0,       
        ),
    )
    return client

def check_model_available(client: httpx.Client, model_name: str) -> bool:
    try:
        response = client.get("/api/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        available_names = [m["name"] for m in models]
        
        return (
            model_name in available_names
            or f"{model_name}:latest" in available_names
        )
    except Exception:
        return False
    
def verify_ollama_models(client: httpx.Client):
    models_to_check = [
        (settings.ollama_model, "генерация текста"),
        (settings.ollama_embed_model, "embeddings"),
    ]

    for model_name, purpose in models_to_check:
        if check_model_available(client, model_name):
            print(f"Model OK: {model_name} ({purpose})")
        else:
            print(f"WARNING: Model '{model_name}' ({purpose}) not found!")
            print(f"  Run: docker exec avatar_ollama ollama pull {model_name}")