from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables."""

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/job_board"
    )
    SECRET_KEY: str = "change-me-in-production"
    GOOGLE_API_KEY: str = ""
    MODEL: str = "gemini-2.5-flash"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ENV: str = "development"

    class Config:
        env_file = ".env"

    @property
    def is_production(self) -> bool:
        return self.ENV.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.ENV.lower() == "development"


settings = Settings()
