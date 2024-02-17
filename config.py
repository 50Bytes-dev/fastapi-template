import os
from functools import lru_cache
from typing import List

from pydantic import PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the FastAPI server.
    Based on pydantic BaseSettings - powerful tool autoload the .env file in the background.
    """

    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    # App

    DEBUG: bool = True
    ALLOW_ORIGINS: List[str]
    ALLOW_ORIGIN_REGEX: str
    APP_PORT: int
    APP_SECRET_KEY: str
    COOKIE_DOMAIN: str

    # Database

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5452"
    POSTGRES_DB: str

    @computed_field
    @property
    def DB_ASYNC_CONNECTION_STR(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=int(self.POSTGRES_PORT),
                path=self.POSTGRES_DB,
            )
        )

    # Redis

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.REDIS_HOST,
                port=int(self.REDIS_PORT),
            )
        )

    # Minio

    MINIO_BUCKET_NAME: str = "media"
    MINIO_HOST: str
    MINIO_BASE_URL: str
    MINIO_VERSION: str = "v1"
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_USE_HTTPS: bool = False

    @computed_field
    @property
    def MINIO_MEDIA_URL(self) -> str:
        return os.path.join(self.MINIO_BASE_URL, self.MINIO_BUCKET_NAME)


@lru_cache()
def get_settings() -> Settings:
    """
    Get settings. ready for FastAPI's Depends.
    lru_cache - cache the Settings object per arguments given.
    """
    settings = Settings()  # type: ignore
    return settings
