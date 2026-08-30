from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./learnpath.db"
    JWT_SECRET: str = 'learnpath-secret-key-change-in-production'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    AI_PROVIDER: str = 'demo'  # 'gemini', 'groq', 'demo'
    AI_API_KEY: str = ''
    DEMO_MODE: bool = True
    FRONTEND_URL: str = 'http://localhost:3000'
    DEBUG: bool = True

    @field_validator("DEBUG", "DEMO_MODE", mode="before")
    @classmethod
    def parse_bool_like(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "production", "prod", "off", "no", "false", "0"}:
                return False
            if normalized in {"debug", "development", "dev", "on", "yes", "true", "1"}:
                return True
        return value

    class Config:
        env_file = ".env"

settings = Settings()
