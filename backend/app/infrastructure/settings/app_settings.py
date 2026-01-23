from typing import no_type_check
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from urllib.parse import quote_plus


@no_type_check
class AppSettings(BaseSettings):
    """Application configuration loaded from environment variables.

    This class loads and validates all infrastructure-level configuration,
    including database credentials for both PostgreSQL roles used by the
    application.

    If any required setting is missing or invalid, application startup
    will fail immediately.
    """

    postgres_host: str
    postgres_port: int = Field(default=5432)
    postgres_app_db: str

    postgres_app_user: str
    postgres_app_user_password: str

    postgres_app_system: str
    postgres_app_system_password: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_access_ttl_seconds: int
    jwt_refresh_ttl_seconds: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def app_user_dsn(self) -> str:
        """Build the async SQLAlchemy DSN for the app_user role.

        Returns:
            str: Async PostgreSQL DSN using the app_user credentials.
        """
        password = quote_plus(self.postgres_app_user_password)

        return (
            "postgresql+asyncpg://"
            f"{self.postgres_app_user}:"
            f"{password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_app_db}"
        )

    def app_system_dsn(self) -> str:
        """Build the async SQLAlchemy DSN for the app_system role.

        Returns:
            str: Async PostgreSQL DSN using the app_system credentials.
        """
        password = quote_plus(self.postgres_app_system_password)

        return (
            "postgresql+asyncpg://"
            f"{self.postgres_app_system}:"
            f"{password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_app_db}"
        )
