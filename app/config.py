"""Application configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # База данных
    database_url: str = "sqlite:///./reviews.db"

    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Reviews Sentiment Service"
    version: str = "1.0.0"

    # Разработка
    debug: bool = False

    # Настройки ML
    use_ml_sentiment: bool = True

    class Config:
        env_file = ".env"


# Глобальный экземпляр настроек
settings = Settings()
