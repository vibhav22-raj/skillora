"""Skills API routes — skill list, user skill gaps, update skill levels."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.database.base import get_db
from app.models import User, Skill, UserSkill, LearnerProfile
from app.schemas import ApiResponse, SkillUpdate
from app.services.auth_service import get_current_user
from app.recommender.skill_gap import calculate_gaps, get_available_roles, get_role_skills

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("/", response_model=ApiResponse)
async def get_skills(
    category: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Get all available skills, optionally filtered by category."""
    query = select(Skill)
    if category:
        query = query.where(Skill.category == category)

    result = await db.execute(query)
    skills = result.scalars().all()

    return ApiResponse(
        success=True,
        data=[
            {
                "id": s.id,
                "name": s.name,
                "category": s.category,
                "description": s.description,
                "difficulty": s.difficulty,
                "prerequisites": s.prerequisites,
                "tags": s.tags,
            }
            for s in skills
        ],
    )


@router.get("/my-skills", response_model=ApiResponse)
async def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's skills with levels."""
    result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == current_user.id)
    )
    user_skills = result.scalars().all()

    return ApiResponse(
        success=True,
        data=[
            {
                "skill_id": us.skill_id,
                "skill_name": us.skill_name,
                "current_level": us.current_level,
                "target_level": us.target_level,
                "gap_score": us.gap_score,
                "priority": us.priority,
            }
            for us in user_skills
        ],
    )


@router.get("/gaps", response_model=ApiResponse)
async def get_skill_gaps(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Calculate and return skill gaps for the user's target role."""
    # Get profile
    profile_result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()

    if not profile or not profile.target_role:
        return ApiResponse(success=True, data=[], message="No target role set")

    # Get user skills
    skills_result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == current_user.id)
    )
    user_skills = skills_result.scalars().all()
    current_skills_dict = {us.skill_name: us.current_level for us in user_skills}

    gaps = calculate_gaps(profile.target_role, current_skills_dict)

    return ApiResponse(success=True, data=gaps)


@router.put("/{skill_name}/level", response_model=ApiResponse)
async def update_skill_level(
    skill_name: str,
    update: SkillUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user's skill level (self-assessment)."""
    # Find existing user skill
    result = await db.execute(
        select(UserSkill).where(
            UserSkill.user_id == current_user.id,
            UserSkill.skill_name == skill_name,
        )
    )
    user_skill = result.scalar_one_or_none()

    if user_skill:
        user_skill.current_level = update.level
    else:
        # Get skill id
        skill_result = await db.execute(select(Skill).where(Skill.name == skill_name))
        skill = skill_result.scalar_one_or_none()

        user_skill = UserSkill(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            skill_id=skill.id if skill else str(uuid.uuid4()),
            skill_name=skill_name,
            current_level=update.level,
            target_level=5,
            gap_score=0.0,
            priority="medium",
        )
        db.add(user_skill)

    await db.commit()
    return ApiResponse(success=True, message=f"Skill level updated to {update.level}/5")


@router.get("/roles", response_model=ApiResponse)
async def get_roles():
    """Get all available career roles."""
    return ApiResponse(success=True, data=get_available_roles())


@router.get("/roles/{role}/requirements", response_model=ApiResponse)
async def get_role_requirements(role: str):
    """Get required skills for a specific role."""
    skills = get_role_skills(role)
    if not skills:
        return ApiResponse(success=False, message="Role not found", data=[])
    return ApiResponse(success=True, data=skills)
