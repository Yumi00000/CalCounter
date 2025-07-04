from datetime import datetime, timedelta
from jose import JWTError, jwt

from backend.app.core.config import settings
from backend.app.databade.schemas.token import TokenData

origins = [
    "http://localhost:27017",
    "http://0.0.0.0:27017",
    "http://localhost:8000",
    "http://0.0.0.0:8000",
]

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(identifier=username)
        return token_data
    except JWTError:
        raise credentials_exception
