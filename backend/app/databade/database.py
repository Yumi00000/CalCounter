from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient

from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


clint = AsyncIOMotorClient(settings.database_url)

db = clint[settings.DB_NAME]
