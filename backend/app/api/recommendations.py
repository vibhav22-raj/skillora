"""Recommendations API routes — scored recommendations and feedback."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime

from backend.app.database.base import get_db
from backend.app.models import User, LearningResource, LearnerProfile, UserSkill, Recommendation, Feedback
from backend.app.schemas import ApiResponse, FeedbackCreate
from backend.app.services.auth_service import get_current_user
from backend.app.recommender.skill_gap import calculate_gaps
from backend.app.recommender.scorer import score_resource
from backend.app.recommender.next_best_action import get_next_best_action
from backend.app.ai.provider_factory import get_ai_provider

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


async def _get_user_context(user: User, db: AsyncSession):
    """Helper to get profile + skills + gaps for scoring."""
    profile_result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == user.id)
    )
    profile = profile_result.scalar_one_or_none()
    profile_dict = {}
    if profile:
        profile_dict = {
            "target_role": profile.target_role or "Software Engineer",
            "experience_level": profile.experience_level or "intermediate",
            "weekly_hours": profile.weekly_hours or 10,
            "learning_style": profile.learning_style or "mixed",
            "preferred_duration": profile.preferred_duration or "medium",
        }

    skills_result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == user.id)
    )
    user_skills = skills_result.scalars().all()
    current_skills_dict = {us.skill_name: us.current_level for us in user_skills}
    user_skill_names = list(current_skills_dict.keys())

    skill_gaps = []
    if profile_dict.get("target_role"):
        skill_gaps = calculate_gaps(profile_dict["target_role"], current_skills_dict)

    return profile_dict, skill_gaps, user_skill_names


@router.get("/", response_model=ApiResponse)
async def get_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get top scored recommendations for the user."""
    profile_dict, skill_gaps, user_skill_names = await _get_user_context(current_user, db)

    # Get all resources
    result = await db.execute(select(LearningResource))
    resources = result.scalars().all()

    # Score each resource
    scored = []
    for resource in resources:
        resource_dict = {
            "id": resource.id,
            "title": resource.title,
            "skills": resource.skills,
            "difficulty": resource.difficulty,
            "duration_hours": resource.duration_hours,
            "format": resource.format,
            "prerequisites": resource.prerequisites,
            "provider": resource.provider,
            "url": resource.url,
            "category": resource.category,
            "rating": resource.rating,
            "is_free": bool(resource.is_free),
            "description": resource.description,
        }
        scores = score_resource(resource_dict, profile_dict, skill_gaps, user_skill_names)
        scored.append({**resource_dict, **scores})

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:limit]

    # Generate explanations using AI (demo mode = instant)
    ai_provider = get_ai_provider()
    for item in top:
        explanation = await ai_provider.generate_explanation({
            "resource": item,
            "profile": profile_dict,
            "skill_gaps": skill_gaps,
        })
        item["explanation"] = explanation

    return ApiResponse(success=True, data=top)


@router.get("/next-best-action", response_model=ApiResponse)
async def get_next_action(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the single best next action for the user."""
    from backend.app.models import Roadmap, Progress as ProgressModel
    profile_dict, skill_gaps, _ = await _get_user_context(current_user, db)

    # Get roadmap phases
    roadmap_result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == current_user.id, Roadmap.is_active == True)
    )
    roadmap = roadmap_result.scalar_one_or_none()
    phases = roadmap.phases if roadmap else []

    # Get recent progress
    progress_result = await db.execute(
        select(ProgressModel).where(ProgressModel.user_id == current_user.id)
    )
    progress_items = progress_result.scalars().all()
    recent_activity = [
        {"resource_id": p.resource_id, "status": p.status, "completion_percentage": p.completion_percentage}
        for p in progress_items
    ]

    action = get_next_best_action(
        profile=profile_dict,
        skill_gaps=skill_gaps,
        progress={},
        roadmap_phases=phases,
        recent_activity=recent_activity,
    )

    return ApiResponse(success=True, data=action)


@router.post("/{resource_id}/feedback", response_model=ApiResponse)
async def submit_feedback(
    resource_id: str,
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit feedback for a recommendation."""
    feedback = Feedback(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        resource_id=resource_id,
        helpful=feedback_data.helpful,
        rating=5 if feedback_data.helpful else 2,
        reason=feedback_data.reason,
        notes=feedback_data.notes,
    )
    db.add(feedback)
    await db.commit()
    return ApiResponse(success=True, message="Feedback recorded. Thank you!")
