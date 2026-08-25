"""Resources API routes — browse, filter, start, complete."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
import uuid
from datetime import datetime

from backend.app.database.base import get_db
from backend.app.models import User, LearningResource, Progress, LearnerProfile, UserSkill
from backend.app.schemas import ApiResponse
from backend.app.services.auth_service import get_current_user
from backend.app.recommender.skill_gap import calculate_gaps
from backend.app.recommender.scorer import score_resource

router = APIRouter(prefix="/api/resources", tags=["resources"])


@router.get("/", response_model=ApiResponse)
async def get_resources(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    category: str = Query(None),
    difficulty: int = Query(None),
    format: str = Query(None),
    search: str = Query(None),
    free_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated, filterable list of learning resources."""
    query = select(LearningResource)

    if category:
        query = query.where(LearningResource.category == category)
    if difficulty:
        query = query.where(LearningResource.difficulty == difficulty)
    if format:
        query = query.where(LearningResource.format == format)
    if free_only:
        query = query.where(LearningResource.is_free == True)
    if search:
        query = query.where(
            or_(
                LearningResource.title.ilike(f"%{search}%"),
                LearningResource.description.ilike(f"%{search}%"),
            )
        )

    result = await db.execute(query)
    all_resources = result.scalars().all()

    # Paginate
    total = len(all_resources)
    start = (page - 1) * per_page
    end = start + per_page
    page_resources = all_resources[start:end]

    data = [_resource_to_dict(r) for r in page_resources]

    return ApiResponse(
        success=True,
        data={
            "resources": data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        },
    )


@router.get("/{resource_id}", response_model=ApiResponse)
async def get_resource(resource_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single resource by ID."""
    result = await db.execute(
        select(LearningResource).where(LearningResource.id == resource_id)
    )
    resource = result.scalar_one_or_none()
    if not resource:
        return ApiResponse(success=False, message="Resource not found")
    return ApiResponse(success=True, data=_resource_to_dict(resource))


@router.post("/{resource_id}/start", response_model=ApiResponse)
async def start_resource(
    resource_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a resource as in-progress."""
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == current_user.id,
            Progress.resource_id == resource_id,
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = Progress(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            resource_id=resource_id,
            status="in_progress",
            completion_percentage=0.0,
            started_at=datetime.utcnow(),
        )
        db.add(progress)
    elif progress.status == "not_started":
        progress.status = "in_progress"
        progress.started_at = datetime.utcnow()

    await db.commit()
    return ApiResponse(success=True, message="Resource started! Good luck!")


@router.post("/{resource_id}/complete", response_model=ApiResponse)
async def complete_resource(
    resource_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a resource as completed."""
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == current_user.id,
            Progress.resource_id == resource_id,
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = Progress(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            resource_id=resource_id,
            status="completed",
            completion_percentage=100.0,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
        )
        db.add(progress)
    else:
        progress.status = "completed"
        progress.completion_percentage = 100.0
        progress.completed_at = datetime.utcnow()

    await db.commit()
    return ApiResponse(success=True, message="🎉 Resource completed! Great work!")


def _resource_to_dict(r: LearningResource) -> dict:
    return {
        "id": r.id,
        "title": r.title,
        "description": r.description,
        "provider": r.provider,
        "url": r.url,
        "category": r.category,
        "skills": r.skills,
        "difficulty": r.difficulty,
        "duration_hours": r.duration_hours,
        "format": r.format,
        "rating": r.rating,
        "tags": r.tags,
        "is_free": bool(r.is_free),
        "prerequisites": r.prerequisites,
    }
