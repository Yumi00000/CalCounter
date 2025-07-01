from datetime import datetime

from pymongo.collection import Collection
from backend.app.databade.schemas.user import UserCreate, UserInDB
from backend.app.databade.database import hash_password, verify_password


def create_user(collection: Collection, user_data: UserCreate) -> str:
    user = UserInDB(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
        active=True,
        age=user_data.age,
        created=datetime.utcnow()
    )

    result = collection.insert_one(user.dict())
    return str(result.inserted_id)


def get_user_by_username_or_email(collection: Collection, identifier: str):
    return collection.find_one({"$or": [{"username": identifier}, {"email": identifier}]})


def auth_user(collection: Collection, identifier: str, password: str):
    user = get_user_by_username_or_email(collection, identifier)
    if user and verify_password(password, user[password]):
        return user

    return None
