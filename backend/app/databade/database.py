from passlib.context import CryptContext
from pymongo import MongoClient
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["sha256_crypt", "bcrypt"], deprecated="bcrypt",)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


client = MongoClient(settings.database_url)
db = client[settings.DB_NAME]
