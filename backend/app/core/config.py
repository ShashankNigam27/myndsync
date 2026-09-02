from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Suraksha Setu"
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "changeme-generate-a-real-secret"
    API_BASE_URL: str = "http://localhost:8000/api/v1"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./myndsync.db"
    DATABASE_POOL_SIZE: int = 10

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"

    # Auth
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_SECRET_KEY: str = "changeme-generate-a-real-secret"

    # Object Storage (raw voice/text — isolated tier)
    OBJECT_STORAGE_ENDPOINT: str = "http://localhost:9000"
    OBJECT_STORAGE_ACCESS_KEY: str = "changeme"
    OBJECT_STORAGE_SECRET_KEY: str = "changeme"
    OBJECT_STORAGE_BUCKET: str = "myndsync-sensitive-store"

    # AI/ML
    NLP_MODEL_NAME: str = "ai4bharat/indic-bert"
    VOICE_STRESS_ENABLED: bool = True
    ESCALATION_MODEL_PATH: str = "./models/escalation_model.pkl"

    # Notifications
    SMS_PROVIDER: str = "mock"
    EMAIL_PROVIDER: str = "smtp"
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = "changeme"
    SMTP_PASSWORD: str = "changeme"

    # Feature flags
    ENABLE_CASE_EVENT_INTEGRATION_SIMULATION: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
