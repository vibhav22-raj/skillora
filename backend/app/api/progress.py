"""Progress API routes — tracking learning progress and streaks."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid
from datetime import datetime, timedelta

from backend.app.database.base import get_db
from backend.app.models import User, Progress, LearningResource, Roadmap
from backend.app.schemas import ApiResponse, ProgressUpdate
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("/", response_model=ApiResponse)
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get overall progress stats for user."""
    result = await db.execute(
        select(Progress).where(Progress.user_id == current_user.id)
    )
    progress_items = result.scalars().all()

    total = len(progress_items)
    completed = sum(1 for p in progress_items if p.status == "completed")
    in_progress = sum(1 for p in progress_items if p.status == "in_progress")
    total_hours = sum(p.time_spent_hours for p in progress_items)

    overall = (completed / total * 100) if total > 0 else 0

    # Calculate streak
    streak = _calculate_streak(progress_items)

    return ApiResponse(
        success=True,
        data={
            "overall_completion": round(overall, 1),
            "total_resources": total,
            "completed_resources": completed,
            "in_progress_resources": in_progress,
            "total_hours_spent": round(total_hours, 1),
            "current_streak": streak,
        },
    )


@router.post("/update", response_model=ApiResponse)
async def update_progress(
    update: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update progress for a resource or project."""
    # Find existing progress
    query = select(Progress).where(Progress.user_id == current_user.id)
    if update.resource_id:
        query = query.where(Progress.resource_id == update.resource_id)
    elif update.project_id:
        query = query.where(Progress.project_id == update.project_id)

    result = await db.execute(query)
    progress = result.scalar_one_or_none()

    if progress:
        progress.status = update.status
        progress.completion_percentage = update.completion_percentage
        progress.time_spent_hours += update.time_spent_hours
        if update.notes:
            progress.notes = update.notes
        if update.status == "completed" and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
    else:
        progress = Progress(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            resource_id=update.resource_id,
            project_id=update.project_id,
            status=update.status,
            completion_percentage=update.completion_percentage,
            time_spent_hours=update.time_spent_hours,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow() if update.status == "completed" else None,
            notes=update.notes,
        )
        db.add(progress)

    await db.commit()
    return ApiResponse(success=True, message="Progress updated!")


@router.get("/streak", response_model=ApiResponse)
async def get_streak(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current learning streak."""
    result = await db.execute(
        select(Progress).where(Progress.user_id == current_user.id)
    )
    progress_items = result.scalars().all()
    streak = _calculate_streak(progress_items)

    return ApiResponse(
        success=True,
        data={"current_streak": streak, "message": f"🔥 {streak} day learning streak!"},
    )


def _calculate_streak(progress_items: list) -> int:
    """Calculate current learning streak in days."""
    if not progress_items:
        return 0

    # Get unique active days
    active_days = set()
    for p in progress_items:
        if p.updated_at:
            active_days.add(p.updated_at.date())
        if p.completed_at:
            active_days.add(p.completed_at.date())

    if not active_days:
        return 0

    today = datetime.utcnow().date()
    streak = 0
    current_day = today

    while current_day in active_days:
        streak += 1
        current_day -= timedelta(days=1)

    return streak
