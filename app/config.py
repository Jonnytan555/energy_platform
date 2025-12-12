from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_USER: str | None = "test"
    DATABASE_PASSWORD: str | None = "test"
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str | None = "test_db"

    SECRET_KEY: str | None = "test"
    ALGORITHM: str | None = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = 60

    API_KEY: str | None = "dummy"

    class Config:
        env_file = ".env"


settings = Settings()