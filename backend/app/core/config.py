from pathlib import Path
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

DIR = Path(__file__).absolute().parent.parent.parent
API_DIR = Path(__file__).absolute().parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)


class UvicornSettings(EnvBaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_NAME: str

    @property
    def database_url(self) -> str:
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASS)
        host = self.DB_HOST
        port = self.DB_PORT
        db_name = self.DB_NAME

        if password:
            return f"mongodb://{user}:{password}@{host}:{port}"
        return f"mongodb://{user}@{host}:{port}/{db_name}"


class HashSettings(EnvBaseSettings):
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class CacheSettings(EnvBaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None = None

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASS:
            return f"redis://{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class Settings(DBSettings, CacheSettings, UvicornSettings, HashSettings):
    SECRET_KEY: str


settings = Settings()
