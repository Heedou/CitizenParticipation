from functools import lru_cache
import os
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "Citizen Participation API")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.database_url = self._normalize_database_url(
            os.getenv("DATABASE_URL", "sqlite:///./citizen_participation.db")
        )
        self.frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
        self.smtp_host = os.getenv("SMTP_HOST", "").strip()
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "").strip()
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").strip().lower() == "true"
        self.mail_from = os.getenv("MAIL_FROM", self.smtp_username).strip()
        self.admin_email = os.getenv("ADMIN_EMAIL", "1coziness@police.go.kr").strip()

    @staticmethod
    def _normalize_database_url(raw_url: str) -> str:
        if raw_url.startswith("postgres://"):
            return raw_url.replace("postgres://", "postgresql+psycopg://", 1)
        if raw_url.startswith("postgresql://"):
            return raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return raw_url

    @property
    def cors_origins(self) -> list[str]:
        if self.frontend_origin.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.frontend_origin.split(",") if origin.strip()]

    @property
    def smtp_configured(self) -> bool:
        return all(
            [
                self.smtp_host,
                self.smtp_port,
                self.smtp_username,
                self.smtp_password,
                self.mail_from,
                self.admin_email,
            ]
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
