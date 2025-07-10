from datetime import datetime

from fastapi import HTTPException, APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import ASCENDING
from starlette import status

from backend.app.databade.crud.user import create_user, auth_user, get_user_data
from backend.app.databade.schemas.user import UserCreate
from backend.app.databade.schemas.user import collection as user_coll
from backend.app.databade.schemas.token import collection as jwt_coll

router = APIRouter(prefix="/user", tags=["users"], )


@router.get("/")
async def root(jwt_token: str = Header(..., alias="Authorization")):
    try:
        token = jwt_token.replace("Bearer ", "") if jwt_token.startswith("Bearer ") else jwt_token
        user_data =get_user_data(user_coll, token)
        return get_user_data(user_coll, token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserCreate):
    email = request.email
    username = request.username
    existing_user = user_coll.find_one({"email": email, "username": username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with that email already exists"
        )

    create_user(user_coll, request)
    return {"msg": "User successfully created"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    try:
        auth_data = auth_user(user_coll, request)

        # Check if a token already exists for the user
        existing_token = jwt_coll.find_one({"user_identifier": request.username})
        token_data = {
            "user_identifier": request.username,
            "access_token": auth_data["access_token"],
            "exp": auth_data["exp"]
        }

        if existing_token:
            jwt_coll.update_one(
                {"user_identifier": request.username},
                {"$set": token_data}
            )
        else:
            jwt_coll.insert_one(token_data)
            ttl_seconds = int((auth_data["exp"] - datetime.now()).total_seconds())
            jwt_coll.create_index([("exp", ASCENDING)], expireAfterSeconds=ttl_seconds)

        return auth_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )