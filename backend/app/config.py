"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings auto-load from .env file or environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database — SQLite by default, swap via env for Postgres in prod
    database_url: str = "sqlite:///./carrier.db"

    # API key required for every endpoint (X-API-Key header)
    api_key: str = "dev_secret_change_me"

    # CORS allowed origins (comma-separated string in env, parsed to list)
    cors_origins: str = "http://localhost:5173,http://localhost:8080"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
