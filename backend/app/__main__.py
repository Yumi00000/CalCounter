import uvicorn
from backend.app.core.config import settings
from backend.app.core.loader import app


if __name__ == "__main__":
    uvicorn.run("backend.app.core.loader:app", host=settings.HOST, port=settings.PORT, reload=True)
