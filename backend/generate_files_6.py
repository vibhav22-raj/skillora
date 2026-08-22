import os

base_dir = r"F:\github clone rep\HCL_Amplified\backend\app"

api_init = ""
with open(os.path.join(base_dir, "api", "__init__.py"), "w") as f:
    f.write(api_init)

auth_router = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserLogin, Token, ApiResponse
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from app.models import User
from sqlalchemy import select

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Dummy DB dependency for now
async def get_db():
    yield None

@router.post("/register", response_model=ApiResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return ApiResponse(success=True, data={"id": "demo-id", "email": user.email})

@router.post("/login", response_model=ApiResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    token = create_access_token({"sub": user.email})
    return ApiResponse(success=True, data={"access_token": token, "token_type": "bearer"})
"""
with open(os.path.join(base_dir, "api", "auth.py"), "w") as f:
    f.write(auth_router)

profile_router = """from fastapi import APIRouter
from app.schemas import ApiResponse
router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/")
async def get_profile():
    return ApiResponse(success=True, data={"target_role": "AI/ML Engineer"})
"""
with open(os.path.join(base_dir, "api", "profile.py"), "w") as f:
    f.write(profile_router)

recommendations_router = """from fastapi import APIRouter
from app.schemas import ApiResponse
router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

@router.get("/")
async def get_recs():
    return ApiResponse(success=True, data=[])
"""
with open(os.path.join(base_dir, "api", "recommendations.py"), "w") as f:
    f.write(recommendations_router)

main_app = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, profile, recommendations
from app.config.settings import settings

app = FastAPI(title="LearnPath AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(recommendations.router)

@app.on_event("startup")
async def startup_event():
    pass
"""
with open(os.path.join(base_dir, "main.py"), "w") as f:
    f.write(main_app)
    
print("API complete.")
