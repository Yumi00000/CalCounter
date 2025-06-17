from fastapi import FastAPI
from redis.asyncio import Redis, ConnectionPool

from backend.app.api.v1 import endpoints
from backend.app.core.config import settings

app = FastAPI()
app.include_router(endpoints.router)

redis_client = Redis(
    connection_pool=ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASS,
        db=0
    ),
)

