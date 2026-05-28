from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType
from app.config import get_settings

settings = get_settings()

@lru_cache()
def get_qdrant_client() -> QdrantClient:
    client = QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        timeout=30,
    )
    return client

def ensure_collection_exists(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection_name in existing:
        print(f"Collection '{settings.qdrant_collection_name}' already exists")
        return

    client.create_collection(
        collection_name=settings.qdrant_collection_name,
        vectors_config=VectorParams(
            size=settings.embedding_dimension,
            distance=Distance.COSINE,
        ),
    )

    client.create_payload_index(
        collection_name=settings.qdrant_collection_name,
        field_name="source",
        field_schema=PayloadSchemaType.KEYWORD,
    )

    print(f"Collection '{settings.qdrant_collection_name}' created")
    print(f"Vector size: {settings.embedding_dimension}, Distance: COSINE")