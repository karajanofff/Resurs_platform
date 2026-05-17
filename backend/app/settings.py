from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./smartkutubxona.db"
    jwt_secret: str = "dev-secret"
    upload_dir: str = "uploads"
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    access_token_minutes: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)


settings = Settings()

