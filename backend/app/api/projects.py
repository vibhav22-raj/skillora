"""Projects API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.base import get_db
from app.models import User, Project, LearnerProfile, UserSkill
from app.schemas import ApiResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=ApiResponse)
async def get_projects(
    category: str = Query(None),
    difficulty: int = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Get all projects with optional filtering."""
    query = select(Project)
    if category:
        query = query.where(Project.category == category)
    if difficulty:
        query = query.where(Project.difficulty == difficulty)

    result = await db.execute(query)
    projects = result.scalars().all()

    return ApiResponse(
        success=True,
        data=[
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "skills": p.skills,
                "difficulty": p.difficulty,
                "duration_hours": p.duration_hours,
                "category": p.category,
                "tags": p.tags,
                "github_template_url": p.github_template_url,
                "domain": p.domain,
                "problem_statement": p.problem_statement,
                "business_value": p.business_value,
                "resume_value": p.resume_value,
                "technologies": p.technologies or [],
                "architecture": p.architecture,
                "resume_bullet": p.resume_bullet,
            }
            for p in projects
        ],
    )


@router.get("/recommended", response_model=ApiResponse)
async def get_recommended_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get projects recommended for the user based on their role and level."""
    profile_result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()

    skills_result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == current_user.id)
    )
    user_skills = skills_result.scalars().all()
    user_skill_names = [us.skill_name for us in user_skills]

    # Get all projects
    projects_result = await db.execute(select(Project))
    all_projects = projects_result.scalars().all()

    # Score projects by genuine skill gap coverage, prerequisite fit, and role relevance
    try:
        from backend.app.recommender.skill_gap import calculate_gaps
    except ImportError:
        from app.recommender.skill_gap import calculate_gaps

    current_skills_dict = {us.skill_name: us.current_level for us in user_skills}
    skill_gaps = []
    if profile and profile.target_role:
        skill_gaps = calculate_gaps(profile.target_role, current_skills_dict)
    
    gap_priorities = {g['skill_name']: g.get('gap', 0) for g in skill_gaps if g.get('gap', 0) > 0}
    exp_level = (profile.experience_level if profile else "beginner") or "beginner"
    target_diff = 2 if exp_level == "beginner" else 3 if exp_level == "intermediate" else 4

    scored = []
    for project in all_projects:
        # Skills the learner already has to build this project
        ready_skills = sum(1 for s in project.skills if current_skills_dict.get(s, 0) >= 2)
        total_skills = len(project.skills) if project.skills else 1
        readiness_score = ready_skills / total_skills

        # Project skills that address active learning gaps
        gap_score = sum(gap_priorities.get(s, 0) for s in project.skills)

        # Difficulty proximity
        diff_fit = 1.0 - (abs(project.difficulty - target_diff) * 0.2)

        # Role relevance
        role_match = 0.0
        tgt = (profile.target_role or "").lower() if profile else ""
        if tgt and project.domain and (tgt in project.domain.lower() or project.domain.lower() in tgt):
            role_match = 1.0
        if tgt and project.title and any(w in project.title.lower() for w in tgt.split()):
            role_match = max(role_match, 0.8)

        # Weighted final score: prioritizing gaps and role fit
        score = (gap_score * 1.2) + (readiness_score * 0.8) + (role_match * 1.5) + (diff_fit * 0.5)
        scored.append((score, project))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_projects = [p for _, p in scored[:6]]

    return ApiResponse(
        success=True,
        data=[
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "skills": p.skills,
                "difficulty": p.difficulty,
                "duration_hours": p.duration_hours,
                "category": p.category,
                "tags": p.tags,
                "github_template_url": p.github_template_url,
                "domain": p.domain,
                "problem_statement": p.problem_statement,
                "business_value": p.business_value,
                "resume_value": p.resume_value,
                "technologies": p.technologies or [],
                "architecture": p.architecture,
                "resume_bullet": p.resume_bullet,
            }
            for p in top_projects
        ],
    )

