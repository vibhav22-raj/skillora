"""Profile API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.database.base import get_db
from app.models import User, LearnerProfile, UserSkill, Skill
from app.schemas import ApiResponse, ProfileUpdate, ProfileOnboarding, ProfileResponse
from app.services.auth_service import get_current_user
from app.ai.provider_factory import get_ai_provider
from app.recommender.skill_gap import calculate_gaps

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("/", response_model=ApiResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's learner profile."""
    result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        return ApiResponse(success=True, data=None, message="No profile found")

    return ApiResponse(
        success=True,
        data=ProfileResponse.model_validate(profile).model_dump(),
    )


@router.put("/", response_model=ApiResponse)
async def update_profile(
    update_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update learner profile."""
    result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        profile = LearnerProfile(id=str(uuid.uuid4()), user_id=current_user.id)
        db.add(profile)

    for field, value in update_data.model_dump(exclude_none=True).items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)

    return ApiResponse(
        success=True,
        data=ProfileResponse.model_validate(profile).model_dump(),
        message="Profile updated successfully",
    )


@router.post("/onboarding", response_model=ApiResponse)
async def complete_onboarding(
    onboarding_data: ProfileOnboarding,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Complete onboarding — creates profile from structured onboarding data.
    Also calculates initial skill gaps and user skills.
    """
    # Update profile
    result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        profile = LearnerProfile(id=str(uuid.uuid4()), user_id=current_user.id)
        db.add(profile)

    profile.target_role = onboarding_data.goal
    profile.experience_level = onboarding_data.experience_level
    profile.weekly_hours = onboarding_data.weekly_hours
    profile.learning_style = onboarding_data.learning_style
    if onboarding_data.target_deadline:
        profile.target_deadline = onboarding_data.target_deadline

    # Save user skills
    current_skills_dict = {s["name"]: s.get("level", 2) for s in onboarding_data.current_skills}

    # Remove old user skills
    from sqlalchemy import delete
    await db.execute(delete(UserSkill).where(UserSkill.user_id == current_user.id))

    # Add new user skills
    for skill_name, level in current_skills_dict.items():
        # Find or skip skill
        skill_result = await db.execute(select(Skill).where(Skill.name == skill_name))
        skill = skill_result.scalar_one_or_none()

        user_skill = UserSkill(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            skill_id=skill.id if skill else str(uuid.uuid4()),
            skill_name=skill_name,
            current_level=level,
            target_level=5,
            gap_score=0.0,
            priority="low",
        )
        db.add(user_skill)

    await db.commit()
    await db.refresh(profile)

    # Calculate skill gaps
    skill_gaps = calculate_gaps(onboarding_data.goal, current_skills_dict)

    return ApiResponse(
        success=True,
        data={
            "profile": ProfileResponse.model_validate(profile).model_dump(),
            "skill_gaps": skill_gaps,
            "skills_count": len(current_skills_dict),
        },
        message="Onboarding complete! Your personalized roadmap is being generated.",
    )


@router.get("/activity", response_model=ApiResponse)
async def get_activity(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get daily learning activity for heatmap (last 365 days)."""
    from app.models import Progress, AssessmentAttempt
    from datetime import date, timedelta
    from collections import defaultdict

    # Get all progress updates
    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == current_user.id)
    )
    progress_items = progress_result.scalars().all()

    # Get assessment attempts
    attempt_result = await db.execute(
        select(AssessmentAttempt).where(AssessmentAttempt.user_id == current_user.id)
    )
    attempts = attempt_result.scalars().all()

    # Build daily activity map
    activity_map = defaultdict(lambda: {"count": 0, "minutes": 0})

    for p in progress_items:
        days_to_check = []
        if p.updated_at:
            days_to_check.append((p.updated_at.date(), max(5, int(p.time_spent_hours * 60))))
        if p.completed_at:
            days_to_check.append((p.completed_at.date(), 30))
        for day, mins in days_to_check:
            key = day.isoformat()
            activity_map[key]["count"] += 1
            activity_map[key]["minutes"] += mins

    for a in attempts:
        if a.completed_at:
            key = a.completed_at.date().isoformat()
            activity_map[key]["count"] += 1
            activity_map[key]["minutes"] += 20

    # For demo user, seed realistic historical activity
    if current_user.is_demo:
        today = date.today()
        import random
        random.seed(42)
        for i in range(180):
            d = today - timedelta(days=i)
            if random.random() > 0.35:
                k = d.isoformat()
                if k not in activity_map or activity_map[k]["count"] == 0:
                    activity_map[k]["count"] = random.randint(1, 4)
                    activity_map[k]["minutes"] = random.randint(15, 90)

    # Calculate current streak
    today = date.today()
    streak = 0
    current_day = today
    while current_day.isoformat() in activity_map:
        streak += 1
        current_day -= timedelta(days=1)

    # Calculate longest streak
    longest_streak = 0
    temp_streak = 0
    prev_day = None
    for day_str in sorted(activity_map.keys()):
        d = date.fromisoformat(day_str)
        if prev_day and (d - prev_day).days == 1:
            temp_streak += 1
        else:
            temp_streak = 1
        if temp_streak > longest_streak:
            longest_streak = temp_streak
        prev_day = d

    return ApiResponse(
        success=True,
        data={
            "activity": dict(activity_map),
            "current_streak": streak,
            "longest_streak": max(longest_streak, streak),
            "total_active_days": len(activity_map),
        },
    )


@router.get("/completed-courses", response_model=ApiResponse)
async def get_completed_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's completed learning resources."""
    from app.models import Progress, LearningResource

    result = await db.execute(
        select(Progress, LearningResource)
        .join(LearningResource, Progress.resource_id == LearningResource.id)
        .where(
            Progress.user_id == current_user.id,
            Progress.status == "completed",
        )
        .order_by(Progress.completed_at.desc())
    )
    rows = result.all()

    completed = []
    for progress, resource in rows:
        completed.append({
            "id": resource.id,
            "title": resource.title,
            "provider": resource.provider,
            "skills": resource.skills,
            "difficulty": resource.difficulty,
            "duration_hours": resource.duration_hours,
            "format": resource.format,
            "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
            "time_spent_hours": progress.time_spent_hours,
        })

    return ApiResponse(success=True, data=completed)

