from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

import os


def _env_file():
    return os.getenv("ENV_FILE", ".env.local")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENV: str = Field("local")
    CELERY_ENABLED: bool = Field(False)

    DATABASE_HOSTNAME: str = Field("localhost")
    DATABASE_PORT: int = Field(5432)
    DATABASE_NAME: str = Field("postgres")
    DATABASE_USER: str = Field("postgres")
    DATABASE_PASSWORD: str = Field("postgres")

    CELERY_BROKER_URL: str = Field("redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field("redis://localhost:6379/1")

    SECRET_KEY: str=Field("supersecret")
    ALGORITHM: str=Field("supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES:int =Field(60)

    API_KEY: str = Field("feafb2b8c51f8a395829cd63e9d7acb26946")

    # --- Redis / Celery ---
    REDIS_HOST: str = Field(default="localhost", alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, alias="REDIS_PORT")

    # --- CORS ---
    cors_origins: str = Field(default="http://localhost,http://localhost:5173", alias="CORS_ORIGINS")

    def cors_list(self) -> List[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]


settings = Settings()
