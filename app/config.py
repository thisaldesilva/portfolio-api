"""Application configuration management."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Environment
    environment: str = "development"

    # Database
    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Polygon/Massive API
    polygon_api_key: str

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""

    # Application
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    workers: int = 4

    # Security
    secret_key: str
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    # Monitoring
    enable_metrics: bool = True

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
