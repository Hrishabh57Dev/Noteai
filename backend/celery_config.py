import os
from celery import Celery
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

# Redis Configuration
redis_client = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True
)

# Celery Configuration
celery_app = Celery(
    "NotesAI",
    broker="redis://localhost:6379/0",  # Redis as the message broker
    backend="redis://localhost:6379/0"  # Redis as the result backend
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True
)

def get_cache(key):
    """Get cached value from Redis"""
    return redis_client.get(key)

def set_cache(key, value, ttl=3600):
    """Set value in Redis cache with optional TTL"""
    redis_client.set(key, value, ex=ttl)

def clear_cache(key):
    """Clear a specific cache key"""
    redis_client.delete(key)
