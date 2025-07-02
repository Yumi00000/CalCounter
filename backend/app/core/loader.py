from fastapi import FastAPI
from redis.asyncio import Redis, ConnectionPool
from starlette.middleware.cors import CORSMiddleware

from backend.app.api.v1.endpoints import get_handlers_router
from backend.app.core.config import settings
from backend.app.middleware.token import origins

app = FastAPI()
app.include_router(get_handlers_router())
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = Redis(
    connection_pool=ConnectionPool(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASS, db=0
    ),
)
