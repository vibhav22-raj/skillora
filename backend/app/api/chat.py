"""Chat API routes — AI mentor conversations."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime

try:
    from backend.app.database.base import get_db
    from backend.app.models import (
        User, ChatSession, ChatMessage, LearnerProfile, UserSkill, Roadmap, AssessmentAttempt,
    )
    from backend.app.schemas import ApiResponse, ChatMessageRequest, ChatSessionCreate
    from backend.app.services.auth_service import get_current_user
    from backend.app.recommender.skill_gap import calculate_gaps
    from backend.app.ai.provider_factory import get_ai_provider
except ImportError:
    from app.database.base import get_db
    from app.models import (
        User, ChatSession, ChatMessage, LearnerProfile, UserSkill, Roadmap, AssessmentAttempt,
    )
    from app.schemas import ApiResponse, ChatMessageRequest, ChatSessionCreate
    from app.services.auth_service import get_current_user
    from app.recommender.skill_gap import calculate_gaps
    from app.ai.provider_factory import get_ai_provider

router = APIRouter(prefix="/api/chat", tags=["chat"])


async def _build_context(user: User, db: AsyncSession) -> dict:
    """Build context dict for AI provider."""
    profile_result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == user.id)
    )
    profile = profile_result.scalar_one_or_none()

    skills_result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == user.id)
    )
    user_skills = skills_result.scalars().all()

    profile_dict = {}
    if profile:
        profile_dict = {
            "target_role": profile.target_role,
            "experience_level": profile.experience_level,
            "weekly_hours": profile.weekly_hours,
            "learning_style": profile.learning_style,
            "career_goal": profile.career_goal,
        }

    current_skills = {us.skill_name: us.current_level for us in user_skills}
    skill_gaps = []
    if profile_dict.get("target_role"):
        skill_gaps = calculate_gaps(profile_dict["target_role"], current_skills)

    roadmap_result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == user.id, Roadmap.is_active == True)
    )
    roadmap = roadmap_result.scalar_one_or_none()
    current_milestone = None
    current_phase = None
    if roadmap:
        phases = roadmap.phases or []
        current_phase = next((p for p in phases if p.get("status") == "in_progress"), None)
        if not current_phase:
            current_phase = next((p for p in phases if p.get("status") != "completed"), phases[0] if phases else None)
        milestones = roadmap.milestones or []
        current_milestone = milestones[0] if milestones else None
        if current_phase and current_phase.get("milestones"):
            current_milestone = {
                "title": current_phase.get("title"),
                "description": current_phase.get("description"),
                "skills": current_phase.get("skills", [])[:4],
            }

    attempt_result = await db.execute(
        select(AssessmentAttempt)
        .where(AssessmentAttempt.user_id == user.id)
        .order_by(AssessmentAttempt.completed_at.desc())
        .limit(1)
    )
    latest_attempt = attempt_result.scalar_one_or_none()
    latest_assessment = None
    if latest_attempt:
        latest_assessment = {
            "score": latest_attempt.score,
            "passed": latest_attempt.passed,
            "skill_estimate": latest_attempt.skill_estimate,
            "completed_at": latest_attempt.completed_at.isoformat() if latest_attempt.completed_at else None,
        }

    try:
        from backend.app.models import Progress, LearningResource
    except ImportError:
        from app.models import Progress, LearningResource

    completed_result = await db.execute(
        select(LearningResource.title)
        .join(Progress, Progress.resource_id == LearningResource.id)
        .where(Progress.user_id == user.id, Progress.status == "completed")
        .limit(5)
    )
    completed_titles = list(completed_result.scalars().all())

    return {
        "profile": profile_dict,
        "skill_gaps": skill_gaps,
        "current_skills": current_skills,
        "completed_resources": completed_titles,
        "roadmap": {
            "title": roadmap.title if roadmap else None,
            "total_weeks": roadmap.total_weeks if roadmap else None,
            "current_phase": current_phase.get("title") if current_phase else None,
        } if roadmap else None,
        "current_milestone": current_milestone,
        "latest_assessment": latest_assessment,
    }


@router.post("/message", response_model=ApiResponse)
async def send_message(
    request: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a message to the AI mentor and get a response."""
    # Get or create session
    session = None
    if request.session_id:
        session_result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == request.session_id,
                ChatSession.user_id == current_user.id,
            )
        )
        session = session_result.scalar_one_or_none()

    if not session:
        session = ChatSession(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message,
        )
        db.add(session)
        await db.flush()

    # Save user message
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session.id,
        role="user",
        content=request.message,
    )
    db.add(user_msg)
    await db.flush()

    # Get conversation history (last 10 messages)
    history_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
    )
    history = list(reversed(history_result.scalars().all()))
    messages = [{"role": m.role, "content": m.content} for m in history]

    # Get context
    context = await _build_context(current_user, db)

    # Generate AI response
    ai_provider = get_ai_provider()
    ai_response = await ai_provider.chat(messages, context)

    # Save AI response
    ai_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session.id,
        role="assistant",
        content=ai_response,
    )
    db.add(ai_msg)
    session.updated_at = datetime.utcnow()
    await db.commit()

    return ApiResponse(
        success=True,
        data={
            "session_id": session.id,
            "message": {
                "id": ai_msg.id,
                "role": "assistant",
                "content": ai_response,
                "created_at": ai_msg.created_at.isoformat(),
            },
        },
    )


@router.get("/sessions", response_model=ApiResponse)
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all chat sessions for current user."""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.updated_at.desc())
        .limit(20)
    )
    sessions = result.scalars().all()

    return ApiResponse(
        success=True,
        data=[
            {
                "id": s.id,
                "title": s.title,
                "created_at": s.created_at.isoformat(),
                "updated_at": s.updated_at.isoformat(),
            }
            for s in sessions
        ],
    )


@router.get("/sessions/{session_id}/messages", response_model=ApiResponse)
async def get_session_messages(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all messages for a chat session."""
    # Verify ownership
    session_result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id,
        )
    )
    session = session_result.scalar_one_or_none()
    if not session:
        return ApiResponse(success=False, message="Session not found")

    msg_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )
    messages = msg_result.scalars().all()

    return ApiResponse(
        success=True,
        data=[
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ],
    )


@router.post("/sessions", response_model=ApiResponse)
async def create_session(
    request: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new chat session."""
    session = ChatSession(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        title=request.title,
    )
    db.add(session)
    await db.commit()

    return ApiResponse(
        success=True,
        data={"id": session.id, "title": session.title},
        message="New conversation started",
    )
