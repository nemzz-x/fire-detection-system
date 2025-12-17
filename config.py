"""Configuration management for Fire Detection System."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # Application Configuration
    app_name: str = "Fire Detection System"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS Configuration
    cors_origins: List[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Storage Configuration
    max_logs: int = 100  # Maximum number of logs to keep in memory
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
