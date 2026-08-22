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

    class Config:
        env_file = ".env"

settings = Settings()
