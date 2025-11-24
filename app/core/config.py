"""Application configuration"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/backupwin_db"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "BackupWin API"
    API_VERSION: str = "1.0.0"

    # Backup Configuration
    DEFAULT_BACKUP_PATH: str = "C:\\Backups"
    MAX_BACKUP_SIZE_GB: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = os.path.join("logs", "app.log")

    # Cloudflare R2 (Optional)
    R2_ACCOUNT_ID: Optional[str] = None
    R2_ACCESS_KEY_ID: Optional[str] = None
    R2_SECRET_ACCESS_KEY: Optional[str] = None
    R2_BUCKET_NAME: Optional[str] = None

    @property
    def backup_path(self) -> Path:
        """Get backup path as Path object"""
        return Path(self.DEFAULT_BACKUP_PATH)


settings = Settings()
