from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from backend.app.databade.crud.user import create_user, auth_user
from backend.app.databade.schemas.user import UserCreate, UserInDB
from backend.app.databade.schemas.user import collection as user_coll
from backend.app.databade.schemas.token import collection as jwt_coll

router = APIRouter(prefix="/user", tags=["users"], )


@router.get("/")
async def root(user_data: UserInDB):
    return user_data


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


@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends()):
    try:
        auth_data = auth_user(user_coll, request)
        token_data = {
            "user_identifier": request.username, **auth_data}
        jwt_coll.insert_one(token_data)
        return auth_data
    except HTTPException:
        raise HTTPException
