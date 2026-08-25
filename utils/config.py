import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def _parse_origins(raw: str) -> list[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


class Settings:
    app_name: str = os.getenv("APP_NAME", "TrustLens")
    app_env: str = os.getenv("APP_ENV", "development")
    cors_origins: list[str] = _parse_origins(
        os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173",
        )
    )
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "10"))
    temp_upload_dir: Path = BASE_DIR / os.getenv("TEMP_UPLOAD_DIR", "temp_uploads")

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


settings = Settings()
settings.temp_upload_dir.mkdir(parents=True, exist_ok=True)
