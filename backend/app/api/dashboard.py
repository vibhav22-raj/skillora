"""Dashboard API — aggregated dashboard data in a single call."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from app.database.base import get_db
from app.models import User, LearnerProfile, UserSkill, Progress, Roadmap, LearningResource
from app.schemas import ApiResponse
from app.services.auth_service import get_current_user
from app.recommender.skill_gap import calculate_gaps
from app.recommender.next_best_action import get_next_best_action, get_today_focus
from app.recommender.scorer import score_resource

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/", response_model=ApiResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return all dashboard data in a single optimized call."""
    # 1. Get profile
    profile_result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()

    profile_dict = {}
    if profile:
        profile_dict = {
            "target_role": profile.target_role,
            "experience_level": profile.experience_level or "intermediate",
            "weekly_hours": profile.weekly_hours or 10.0,
            "learning_style": profile.learning_style or "mixed",
            "preferred_duration": profile.preferred_duration or "medium",
        }

    # 2. Get user skills
    skills_result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == current_user.id)
    )
    user_skills = skills_result.scalars().all()
    current_skills_dict = {us.skill_name: us.current_level for us in user_skills}

    # 3. Calculate skill gaps
    skill_gaps = []
    if profile_dict.get("target_role"):
        skill_gaps = calculate_gaps(profile_dict["target_role"], current_skills_dict)

    # 4. Get progress
    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == current_user.id)
    )
    progress_items = progress_result.scalars().all()
    total = len(progress_items)
    completed = sum(1 for p in progress_items if p.status == "completed")
    in_progress_count = sum(1 for p in progress_items if p.status == "in_progress")
    total_hours = sum(p.time_spent_hours for p in progress_items)
    overall_progress = round((completed / total * 100) if total > 0 else 0, 1)

    # 5. Calculate streak
    streak = _calculate_streak(progress_items)

    # 6. Get roadmap
    roadmap_result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == current_user.id, Roadmap.is_active == True)
    )
    roadmap = roadmap_result.scalar_one_or_none()
    phases = roadmap.phases if roadmap else []

    # 7. Current milestone
    current_milestone = None
    if roadmap and roadmap.milestones:
        current_milestone = roadmap.milestones[0] if roadmap.milestones else None

    # 8. Next best action
    recent_activity = [
        {
            "resource_id": p.resource_id,
            "status": p.status,
            "completion_percentage": p.completion_percentage,
        }
        for p in progress_items
    ]

    next_action = get_next_best_action(
        profile=profile_dict,
        skill_gaps=skill_gaps,
        progress={"phase_completion": overall_progress / 100},
        roadmap_phases=phases,
        recent_activity=recent_activity,
    )

    # 9. Today's focus
    today_focus = get_today_focus(
        profile=profile_dict,
        roadmap_phases=phases,
        available_hours=(profile_dict.get("weekly_hours", 10) / 5),
    )

    # 10. Weekly activity (last 7 days)
    weekly_activity = _get_weekly_activity(progress_items)

    # 11. Top recommendations (fast — no AI call needed for dashboard)
    top_resources = []
    if profile_dict:
        resources_result = await db.execute(select(LearningResource).limit(50))
        resources = resources_result.scalars().all()
        user_skill_names = list(current_skills_dict.keys())

        scored = []
        for r in resources:
            r_dict = {
                "id": r.id, "title": r.title, "skills": r.skills,
                "difficulty": r.difficulty, "duration_hours": r.duration_hours,
                "format": r.format, "prerequisites": r.prerequisites,
                "provider": r.provider, "url": r.url, "category": r.category,
                "rating": r.rating, "description": r.description,
            }
            scores = score_resource(r_dict, profile_dict, skill_gaps, user_skill_names)
            scored.append({**r_dict, **scores})

        scored.sort(key=lambda x: x["score"], reverse=True)
        top_resources = scored[:3]

    return ApiResponse(
        success=True,
        data={
            "user_name": current_user.name,
            "target_role": profile_dict.get("target_role"),
            "overall_progress": overall_progress,
            "current_streak": streak,
            "hours_learned": round(total_hours, 1),
            "skills_improved": len([us for us in user_skills if us.current_level > 0]),
            "completed_resources": completed,
            "in_progress_resources": in_progress_count,
            "next_best_action": next_action,
            "today_focus": today_focus,
            "skill_gaps": skill_gaps[:8],  # Top 8 for radar chart
            "weekly_activity": weekly_activity,
            "current_milestone": current_milestone,
            "recent_recommendations": top_resources,
            "roadmap_summary": {
                "total_phases": len(phases),
                "total_weeks": roadmap.total_weeks if roadmap else 0,
                "title": roadmap.title if roadmap else None,
            },
        },
    )


def _calculate_streak(progress_items: list) -> int:
    """Calculate current learning streak."""
    if not progress_items:
        return 0

    active_days = set()
    for p in progress_items:
        if p.updated_at:
            active_days.add(p.updated_at.date())
        if p.completed_at:
            active_days.add(p.completed_at.date())

    today = datetime.utcnow().date()
    streak = 0
    current_day = today

    while current_day in active_days:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def _get_weekly_activity(progress_items: list) -> list:
    """Generate last 7 days activity data."""
    from collections import defaultdict

    activity_by_day = defaultdict(lambda: {"hours": 0.0, "resources_completed": 0})

    for p in progress_items:
        if p.updated_at:
            day_key = p.updated_at.strftime("%a")
            activity_by_day[day_key]["hours"] += p.time_spent_hours
            if p.status == "completed":
                activity_by_day[day_key]["resources_completed"] += 1

    # Build last 7 days
    days = []
    today = datetime.utcnow()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_name = day.strftime("%a")
        data = activity_by_day.get(day_name, {"hours": 0.0, "resources_completed": 0})
        days.append({
            "day": day_name,
            "date": day.strftime("%Y-%m-%d"),
            "hours": round(data["hours"], 1),
            "resources_completed": data["resources_completed"],
        })

    return days
