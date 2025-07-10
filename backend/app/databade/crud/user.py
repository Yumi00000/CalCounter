from datetime import datetime

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.synchronous.collection import Collection
from starlette import status

from backend.app.databade.schemas.user import UserCreate, UserInDB, UserPublic
from backend.app.middleware.password_hash import hash_password, verify_password
from backend.app.middleware.token import create_access_token, verify_token

def create_user(collection: Collection, user_data: UserCreate, ) -> str:
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


def auth_user(collection: Collection, login_data: OAuth2PasswordRequestForm) -> dict:
    user = collection.find_one({"username": login_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user found with this {login_data.username} username')
    if not verify_password(login_data.password, user["password"], ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Wrong Username or password')
    access_token, exp = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer", "exp": exp}


def get_user_data(collection: Collection, token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the token first
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)

    # Query user collection using the username from the token
    user = collection.find_one({"username": token_data.identifier})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found for username: {token_data.identifier}"
        )
    return UserPublic(**user)
