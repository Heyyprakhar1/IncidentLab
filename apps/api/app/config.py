"""
Application configuration.

Purpose
-------
Provide centralized application configuration using environment variables.

Responsibilities
----------------
- Load configuration from environment variables.
- Provide typed application settings.
- Expose a single shared settings instance.

Non-Responsibilities
--------------------
- Business logic.
- Database connections.
- Application lifecycle management.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "IncidentLab API"

    app_description: str = (
        "Cloud-native incident response and investigation platform."
    )

    app_version: str = "0.7.0"

    app_env: str = "development"

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    log_level: str = "INFO"

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    db_host: str = "localhost"

    db_port: int = 5432

    db_name: str = "incidentlab"

    db_user: str = "postgres"

    db_password: str = "postgres"

    @property
    def database_url(self) -> str:
        """
        Return the SQLAlchemy async database URL.
        """

        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    jwt_secret_key: str = "CHANGE_ME_IN_PRODUCTION"

    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    # ------------------------------------------------------------------
    # Environment Configuration
    # ------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
