import os

base_dir = r"F:\github clone rep\HCL_Amplified\backend"

dirs = [
    "app", "app/config", "app/models", "app/schemas", "app/api", 
    "app/services", "app/ai", "app/recommender", "app/database", "app/utils",
    "tests"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    init_file = os.path.join(base_dir, d, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            pass

reqs = """fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0
pydantic>=2.7.0
pydantic-settings>=2.3.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9
httpx>=0.27.0
aiohttp>=3.9.0
google-generativeai>=0.7.0
groq>=0.9.0
python-dotenv>=1.0.1
slowapi>=0.1.9
loguru>=0.7.2
pytest>=8.2.0
pytest-asyncio>=0.23.0
aiosqlite>=0.20.0
"""
with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
    f.write(reqs)

env_example = """DATABASE_URL=sqlite+aiosqlite:///./learnpath.db
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
AI_PROVIDER=demo
AI_API_KEY=
DEMO_MODE=true
FRONTEND_URL=http://localhost:3000
DEBUG=true
"""
with open(os.path.join(base_dir, ".env.example"), "w") as f:
    f.write(env_example)

dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
with open(os.path.join(base_dir, "Dockerfile"), "w") as f:
    f.write(dockerfile)

settings = """from pydantic_settings import BaseSettings

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
"""
with open(os.path.join(base_dir, "app/config/settings.py"), "w") as f:
    f.write(settings)

print("Basic setup complete.")
