"""Projects API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database.base import get_db
from backend.app.models import User, Project, LearnerProfile, UserSkill
from backend.app.schemas import ApiResponse
from backend.app.services.auth_service import get_current_user

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

    # Score projects by skill overlap, gap coverage and role relevance
    from backend.app.recommender.skill_gap import calculate_gaps

    current_skills_dict = {s: 0 for s in user_skill_names}
    skill_gaps = []
    if profile and profile.target_role:
        skill_gaps = calculate_gaps(profile.target_role, current_skills_dict)
    gap_skill_names = [g['skill_name'] for g in skill_gaps[:5]]

    scored = []
    for project in all_projects:
        overlap = sum(1 for s in project.skills if s in user_skill_names)
        total_skills = len(project.skills) if project.skills else 1
        overlap_score = overlap / total_skills

        # How many project skills cover the user's high-priority gaps
        gap_coverage = sum(1 for s in project.skills if s in gap_skill_names)

        # Role/domain match heuristic
        role_match = 0
        tgt = (profile.target_role or "").lower() if profile else ""
        if tgt and project.domain and tgt in (project.domain or "").lower():
            role_match = 1
        if tgt and project.title and tgt in project.title.lower():
            role_match = max(role_match, 1)

        # Weighted score
        score = overlap_score + (gap_coverage * 0.8) + (role_match * 0.5)
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

