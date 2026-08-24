"""Learning Path API routes — generate, get, adapt roadmaps."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid
from datetime import datetime

from backend.app.database.base import get_db
from backend.app.models import User, LearnerProfile, UserSkill, LearningResource, Roadmap, Project
from backend.app.schemas import ApiResponse, LearningPathGenerate, LearningPathAdapt
from backend.app.services.auth_service import get_current_user
from backend.app.recommender.skill_gap import calculate_gaps
from backend.app.recommender.roadmap_generator import generate_roadmap, adapt_roadmap_for_time_change
from backend.app.recommender.scorer import score_resource
from backend.app.ai.provider_factory import get_ai_provider

router = APIRouter(prefix="/api/learning-path", tags=["learning-path"])


async def _enrich_phases_with_resources(phases: list, resources: list, projects: list, profile_dict: dict, skill_gaps: list, user_skill_names: list):
    """Attach actual resource objects to phases based on skill matching."""
    # Score resources
    scored_resources = []
    for r in resources:
        r_dict = {
            "id": r.id, "title": r.title, "skills": r.skills,
            "difficulty": r.difficulty, "duration_hours": r.duration_hours,
            "format": r.format, "prerequisites": r.prerequisites,
        }
        scores = score_resource(r_dict, profile_dict, skill_gaps, user_skill_names)
        scored_resources.append({**r_dict, "score": scores["score"]})

    scored_resources.sort(key=lambda x: x["score"], reverse=True)

    # Assign resources to phases by skill matching
    for phase in phases:
        phase_skills = phase.get("skills", [])
        phase_resources = []
        for sr in scored_resources:
            if any(s in sr.get("skills", []) for s in phase_skills):
                phase_resources.append(sr)
                if len(phase_resources) >= 3:
                    break

        # If no match, take top resources
        if not phase_resources:
            phase_resources = scored_resources[:2]

        phase["resources"] = phase_resources

    return phases


@router.post("/generate", response_model=ApiResponse)
async def generate_learning_path(
    request: LearningPathGenerate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a personalized learning roadmap."""
    # Allow free-text goal extraction via AI provider if provided
    goal = request.goal
    experience_level = request.experience_level
    weekly_hours = request.weekly_hours
    learning_style = request.learning_style
    current_skills_dict = {s["name"]: s.get("level", 2) for s in request.current_skills}

    if getattr(request, "free_text_goal", None):
        ai_provider = get_ai_provider()
        try:
            extracted = await ai_provider.extract_profile(request.free_text_goal)
            if extracted:
                # Merge extracted fields, prefer AI when available
                goal = extracted.get("target_role") or goal
                experience_level = extracted.get("experience_level") or experience_level
                weekly_hours = extracted.get("weekly_hours") or weekly_hours
                learning_style = extracted.get("learning_style") or learning_style
                # Merge skills: extracted current_skills may be dict -> {name: level}
                ext_skills = extracted.get("current_skills") or {}
                if isinstance(ext_skills, dict):
                    for k, v in ext_skills.items():
                        if k and isinstance(v, (int, float)):
                            current_skills_dict[k] = int(v)
        except Exception:
            # Fallback: use DemoProvider heuristic if AI fails
            from backend.app.ai.demo_provider import DemoProvider
            demo = DemoProvider()
            try:
                extracted = await demo.extract_profile(request.free_text_goal)
                goal = extracted.get("target_role") or goal
                experience_level = extracted.get("experience_level") or experience_level
                weekly_hours = extracted.get("weekly_hours") or weekly_hours
                learning_style = extracted.get("learning_style") or learning_style
                ext_skills = extracted.get("current_skills") or {}
                if isinstance(ext_skills, dict):
                    for k, v in ext_skills.items():
                        if k and isinstance(v, (int, float)):
                            current_skills_dict[k] = int(v)
            except Exception:
                pass

    # Build profile dict
    profile_dict = {
        "target_role": goal,
        "experience_level": experience_level,
        "weekly_hours": weekly_hours,
        "learning_style": learning_style,
        "preferred_duration": "medium",
    }

    user_skill_names = list(current_skills_dict.keys())

    # Calculate gaps
    skill_gaps = calculate_gaps(goal, current_skills_dict)

    # Parse deadline
    deadline_months = None
    if request.target_deadline:
        try:
            deadline_months = int(request.target_deadline.replace("months", "").strip())
        except Exception:
            pass

    # Generate roadmap
    roadmap_data = generate_roadmap(
        target_role=request.goal,
        skill_gaps=skill_gaps,
        weekly_hours=request.weekly_hours,
        target_deadline_months=deadline_months,
        learning_style=request.learning_style,
        current_skills=current_skills_dict,
    )

    # Get resources and projects for enrichment
    resources_result = await db.execute(select(LearningResource))
    resources = resources_result.scalars().all()

    projects_result = await db.execute(select(Project))
    projects = projects_result.scalars().all()

    # Enrich phases with actual resources
    roadmap_data["phases"] = await _enrich_phases_with_resources(
        roadmap_data["phases"], resources, projects, profile_dict, skill_gaps, user_skill_names
    )

    # Save to DB
    await db.execute(
        delete(Roadmap).where(Roadmap.user_id == current_user.id, Roadmap.is_active == True)
    )

    roadmap = Roadmap(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        title=roadmap_data["title"],
        description=roadmap_data["description"],
        total_weeks=roadmap_data["total_weeks"],
        phases=roadmap_data["phases"],
        milestones=roadmap_data["milestones"],
        is_active=True,
    )
    db.add(roadmap)

    # Update profile
    profile_result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    if profile:
        profile.target_role = request.goal
        profile.experience_level = request.experience_level
        profile.weekly_hours = request.weekly_hours
        profile.learning_style = request.learning_style

    await db.commit()
    await db.refresh(roadmap)

    return ApiResponse(
        success=True,
        data={
            "roadmap": {
                "id": roadmap.id,
                "title": roadmap.title,
                "description": roadmap.description,
                "total_weeks": roadmap.total_weeks,
                "phases": roadmap.phases,
                "milestones": roadmap.milestones,
            },
            "skill_gaps": skill_gaps,
        },
        message=f"Your personalized {request.goal} roadmap is ready!",
    )


@router.get("/", response_model=ApiResponse)
async def get_learning_path(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's current active roadmap."""
    result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == current_user.id, Roadmap.is_active == True)
    )
    roadmap = result.scalar_one_or_none()

    if not roadmap:
        return ApiResponse(success=True, data=None, message="No roadmap found")

    return ApiResponse(
        success=True,
        data={
            "id": roadmap.id,
            "title": roadmap.title,
            "description": roadmap.description,
            "total_weeks": roadmap.total_weeks,
            "phases": roadmap.phases,
            "milestones": roadmap.milestones,
            "generated_at": roadmap.generated_at.isoformat(),
        },
    )


@router.post("/adapt", response_model=ApiResponse)
async def adapt_learning_path(
    adapt_request: LearningPathAdapt,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Adapt roadmap based on user feedback.
    THE WOW FEATURE — dynamically recalculates timeline.
    """
    result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == current_user.id, Roadmap.is_active == True)
    )
    roadmap = result.scalar_one_or_none()

    if not roadmap:
        return ApiResponse(success=False, message="No active roadmap found")

    # Use AI to interpret feedback
    ai_provider = get_ai_provider()

    profile_result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    profile_dict = {"target_role": profile.target_role if profile else "Software Engineer"}

    interpretation = await ai_provider.interpret_feedback(
        adapt_request.feedback, {"profile": profile_dict}
    )

    # Apply adaptation
    phases = roadmap.phases
    adaptation_message = interpretation.get("message", "Roadmap adapted based on your feedback.")
    new_weekly_hours = None

    action = interpretation.get("action", "acknowledge")

    if action == "reduce_weekly_hours":
        new_weekly_hours = interpretation.get("new_weekly_hours", 5.0)
        roadmap_dict = {"phases": phases, "weekly_hours": profile.weekly_hours if profile else 10.0}
        adapted = adapt_roadmap_for_time_change(roadmap_dict, new_weekly_hours)
        phases = adapted["phases"]
        if profile:
            profile.weekly_hours = new_weekly_hours
        adaptation_message = f"✅ I've extended your timeline from {roadmap.total_weeks} weeks to {adapted['total_weeks']} weeks and prioritized the highest-impact skills to fit your {new_weekly_hours}h/week schedule."
        roadmap.total_weeks = adapted["total_weeks"]

    elif action == "increase_weekly_hours":
        new_weekly_hours = interpretation.get("new_weekly_hours", 20.0)
        roadmap_dict = {"phases": phases, "weekly_hours": profile.weekly_hours if profile else 10.0}
        adapted = adapt_roadmap_for_time_change(roadmap_dict, new_weekly_hours)
        phases = adapted["phases"]
        if profile:
            profile.weekly_hours = new_weekly_hours
        adaptation_message = f"🚀 Great! I've optimized your roadmap for {new_weekly_hours}h/week. Your new estimated completion is {adapted['total_weeks']} weeks."
        roadmap.total_weeks = adapted["total_weeks"]

    roadmap.phases = phases
    roadmap.updated_at = datetime.utcnow()
    await db.commit()

    return ApiResponse(
        success=True,
        data={
            "roadmap": {
                "id": roadmap.id,
                "title": roadmap.title,
                "total_weeks": roadmap.total_weeks,
                "phases": roadmap.phases,
            },
            "adaptation": interpretation,
        },
        message=adaptation_message,
    )
