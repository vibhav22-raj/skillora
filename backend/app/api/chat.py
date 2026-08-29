"""Chat API routes — AI mentor conversations."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime

from app.database.base import get_db
from app.models import User, ChatSession, ChatMessage, LearnerProfile, UserSkill, Roadmap
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
        }

    current_skills = {us.skill_name: us.current_level for us in user_skills}
    skill_gaps = []
    if profile_dict.get("target_role"):
        skill_gaps = calculate_gaps(profile_dict["target_role"], current_skills)

    # Include user's active roadmap and a short roadmap summary so AI can reference current phase/progress
    roadmap_summary = None
    roadmap_result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == user.id, Roadmap.is_active == True)
    )
    roadmap = roadmap_result.scalar_one_or_none()
    if roadmap:
        total_phases = len(roadmap.phases) if roadmap.phases else 0
        # attempt to determine current phase by status or first in_progress
        current_phase = None
        if roadmap.phases:
            for p in roadmap.phases:
                if p.get('status') == 'in_progress':
                    current_phase = p
                    break
            if not current_phase and len(roadmap.phases) > 0:
                # fallback: first phase
                current_phase = roadmap.phases[0]
        roadmap_summary = {
            "id": roadmap.id,
            "title": roadmap.title,
            "total_phases": total_phases,
            "total_weeks": getattr(roadmap, 'total_weeks', None),
            "current_phase": current_phase,
        }

    return {"profile": profile_dict, "skill_gaps": skill_gaps, "roadmap": roadmap_summary}


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
