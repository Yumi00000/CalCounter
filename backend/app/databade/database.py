from pymongo import MongoClient
from backend.app.core.config import settings

client = MongoClient(settings.database_url)
db = client[settings.DB_NAME]
