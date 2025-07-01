from fastapi import APIRouter

from backend.app.databade.crud import create_user
from backend.app.databade.database import db
from backend.app.databade.schemas.user import UserCreate

router = APIRouter()


@router.get("/")
async def root():
    return {"hello": "world"}

@router.post("/register")
async def register(**user_data:UserCreate):
    try:
        collection = db["users"]
        create_user(collection, **user_data)
        return {"msg":"User successfully created", "status_code":"200"}
    except ValueError as e:
        print(e)