"""Auth API routes — register, login, logout, me."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from backend.app.database.base import get_db
from backend.app.models import User, LearnerProfile
from backend.app.schemas import UserCreate, UserLogin, ApiResponse, UserResponse
from backend.app.services.auth_service import (
    get_password_hash, verify_password, create_access_token, get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    # Check if email exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        id=str(uuid.uuid4()),
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    db.add(user)
    await db.flush()

    # Create empty profile
    profile = LearnerProfile(
        id=str(uuid.uuid4()),
        user_id=user.id,
    )
    db.add(profile)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"sub": user.id})
    return ApiResponse(
        success=True,
        data={"user": UserResponse.model_validate(user).model_dump(), "access_token": token, "token_type": "bearer"},
        message="Registration successful",
    )


@router.post("/login", response_model=ApiResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login with email and password."""
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is inactive")

    token = create_access_token({"sub": user.id})
    return ApiResponse(
        success=True,
        data={"user": UserResponse.model_validate(user).model_dump(), "access_token": token, "token_type": "bearer"},
        message="Login successful",
    )


@router.get("/me", response_model=ApiResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return ApiResponse(
        success=True,
        data=UserResponse.model_validate(current_user).model_dump(),
    )


@router.post("/logout", response_model=ApiResponse)
async def logout():
    """Logout (client-side token removal)."""
    return ApiResponse(success=True, message="Logged out successfully")
