from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

DIR = Path(__file__).absolute().parent.parent.parent
API_DIR = Path(__file__).absolute().parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)


class UvicornSettings(EnvBaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DBSettings(EnvBaseSettings):
    DB_HOST: str = "MOGO_HOST"
    DB_USER: str = "MONGO_USERNAME"
    DB_PASS: str = "MONGO_PASSWORD"
    DB_PORT: str = "MONGO_PORT"
    DB_NAME: str = "MONGO_NAME"

    @property
    def database_url(self) -> "URL | str":
        if self.DB_PASS:
            return f"mongodb://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"mongodb://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class CacheSettings(EnvBaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None = None

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASS:
            return f"redis://{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class Settings(DBSettings, CacheSettings, UvicornSettings):
    SENTRY_DSN: str | None = None


settings = Settings()
