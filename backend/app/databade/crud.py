from datetime import timezone

from motor.motor_asyncio import AsyncIOMotorCollection

from backend.app.databade.database import hash_password, verify_password


async def create_user(collection: AsyncIOMotorCollection, user_data: dict) -> str:
    user = {**user_data, "password": hash_password(user_data["password"]), "created": timezone.utc, "active": True}

    result = await collection.insert_one(user)
    return str(result.inserted_id)


async def get_user_by_username_or_email(collection: AsyncIOMotorCollection, identifier: str):
    return await collection.find_one({"$or": [{"username": identifier}, {"email": identifier}]})


async def auth_user(collection: AsyncIOMotorCollection, identifier: str, password: str):
    user = await get_user_by_username_or_email(collection, identifier)
    if user and verify_password(password, user[password]):
        return user

    return None
