from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settigns(BaseSettings):
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "avatar_messages"

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_embed_model: str = "nomic-embed-text"

    embedding_dimension: int = 768

    retrieval_top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  
    )

@lru_cache
def get_settings() -> Settigns:
    return Settigns()