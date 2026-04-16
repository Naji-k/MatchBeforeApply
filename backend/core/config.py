from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import computed_field

_ENV_FILE = str(Path(__file__).resolve().parent.parent / ".env")


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables."""

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/job_board"
    )
    SECRET_KEY: str = "change-me-in-production"
    GOOGLE_API_KEY: str = ""
    GOOGLE_CLIENT_ID: str = ""
    MODEL: str = "gemini-2.5-flash"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ENV: str = "development"
    DEMO_USER: int | None = None
    RESEND_TOKEN: str = ""
    RESEND_FROM_EMAIL: str = "noreply@matchbeforeapply.com"

    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    class Config:
        env_file = _ENV_FILE

    @property
    def is_production(self) -> bool:
        return self.ENV.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.ENV.lower() == "development"


settings = Settings()
