import uvicorn
from fastapi.security import OAuth2PasswordBearer

from backend.app.core.config import settings
from backend.app.core.loader import app

if __name__ == "__main__":
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    uvicorn.run("backend.app.core.loader:app", host=settings.HOST, port=settings.PORT, reload=True)
