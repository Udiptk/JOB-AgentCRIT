from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./jobagent.db"

    # Server
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Security
    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Scraping
    SCRAPER_DELAY_SECONDS: int = 2
    MAX_JOBS_PER_SOURCE: int = 50


settings = Settings()
