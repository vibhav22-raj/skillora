"""
LearnPath AI — FastAPI Application Entry Point
Production-ready AI-powered personalized learning path recommender.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging

try:
    from backend.app.config.settings import settings
    from backend.app.database.base import create_tables
    from backend.app.api import skills, assessment, auth, chat, dashboard, learning_path, profile, progress, projects, recommendations, resources
except ImportError:
    from app.config.settings import settings
    from app.database.base import create_tables
    from app.api import skills, assessment, auth, chat, dashboard, learning_path, profile, progress, projects, recommendations, resources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    logger.info("🚀 LearnPath AI starting up...")
    logger.info(f"AI Provider: {settings.AI_PROVIDER}")
    logger.info(f"Demo Mode: {settings.DEMO_MODE}")
    logger.info(f"Database: {settings.DATABASE_URL[:50]}...")

    # Create database tables
    await create_tables()
    logger.info("✅ Database tables created")

    try:
        try:
            from backend.app.database.seed_data import seed_database
        except ImportError:
            from app.database.seed_data import seed_database
        await seed_database()
        logger.info("✅ Seed data loaded")
    except Exception as e:
        logger.warning(f"⚠️  Seed data warning: {e}")

    yield

    logger.info("👋 LearnPath AI shutting down...")


# Create FastAPI app
app = FastAPI(
    title="LearnPath AI",
    description="AI-Powered Personalized Learning Path Recommender",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request Timing Middleware ─────────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "ms"
    return response


# ─── Global Exception Handler ──────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "message": "Something went wrong. Your data is safe. Please try again.",
        },
    )


# ─── Include Routers ───────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(learning_path.router)
app.include_router(recommendations.router)
app.include_router(skills.router)
app.include_router(resources.router)
app.include_router(projects.router)
app.include_router(assessment.router)
app.include_router(chat.router)
app.include_router(progress.router)
app.include_router(dashboard.router)


# ─── Health Check ──────────────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "LearnPath AI",
        "version": "1.0.0",
        "ai_provider": settings.AI_PROVIDER,
        "demo_mode": settings.DEMO_MODE,
    }


@app.get("/")
async def root():
    return {
        "message": "Welcome to LearnPath AI API",
        "docs": "/docs",
        "health": "/health",
    }
