from typing import Any
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator, ValidationInfo

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Loopback'
    API_V1_STR: str = '/api/v1'
    DEBUG: bool = bool(int(os.environ.get('DEBUG', 0)))

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int | None
    POSTGRES_DB: str
    DATABASE_URL: PostgresDsn | None = None

    @field_validator('DATABASE_URL', mode="before")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:

        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            port=values.data.get("POSTGRES_PORT", 5432),
            path=f'{values.data.get("POSTGRES_DB")}',
        )


settings = Settings()