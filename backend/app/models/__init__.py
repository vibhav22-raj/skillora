"""All SQLAlchemy ORM models for LearnPath AI."""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
import uuid
from backend.app.database.base import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship("LearnerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True)
    target_role: Mapped[str] = mapped_column(String(255), nullable=True)
    experience_level: Mapped[str] = mapped_column(String(50), nullable=True)  # beginner/intermediate/advanced
    education: Mapped[str] = mapped_column(String(255), nullable=True)
    career_goal: Mapped[str] = mapped_column(Text, nullable=True)
    weekly_hours: Mapped[float] = mapped_column(Float, nullable=True, default=10.0)
    learning_style: Mapped[str] = mapped_column(String(50), nullable=True, default="mixed")
    target_deadline: Mapped[str] = mapped_column(String(50), nullable=True)
    preferred_duration: Mapped[str] = mapped_column(String(50), nullable=True, default="medium")
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    weaknesses: Mapped[list] = mapped_column(JSON, default=list)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_image: Mapped[str] = mapped_column(Text, nullable=True)  # Base64 encoded image or URL
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    prerequisites: Mapped[list] = mapped_column(JSON, default=list)
    tags: Mapped[list] = mapped_column(JSON, default=list)


class UserSkill(Base):
    __tablename__ = "user_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    skill_id: Mapped[str] = mapped_column(String(36), ForeignKey("skills.id"))
    skill_name: Mapped[str] = mapped_column(String(255), nullable=True)  # denormalized for speed
    current_level: Mapped[int] = mapped_column(Integer, default=0)  # 0-5
    target_level: Mapped[int] = mapped_column(Integer, default=0)  # 0-5
    gap_score: Mapped[float] = mapped_column(Float, default=0.0)
    priority: Mapped[str] = mapped_column(String(20), default="low")  # low/medium/high/critical
    last_assessed: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    provider: Mapped[str] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(1000))
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    skills: Mapped[list] = mapped_column(JSON, default=list)  # list of skill names
    difficulty: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    duration_hours: Mapped[float] = mapped_column(Float, default=1.0)
    format: Mapped[str] = mapped_column(String(50), nullable=True)  # video/article/course/interactive
    rating: Mapped[float] = mapped_column(Float, default=4.0)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)
    prerequisites: Mapped[list] = mapped_column(JSON, default=list)  # list of skill names


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    skills: Mapped[list] = mapped_column(JSON, default=list)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    duration_hours: Mapped[float] = mapped_column(Float, default=8.0)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    github_template_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    # Industry metadata
    domain: Mapped[str] = mapped_column(String(100), nullable=True)  # AI/ML, Web, Data, DevOps, etc.
    problem_statement: Mapped[str] = mapped_column(Text, nullable=True)
    business_value: Mapped[str] = mapped_column(Text, nullable=True)
    resume_value: Mapped[str] = mapped_column(String(20), nullable=True)  # High/Medium/Low
    technologies: Mapped[list] = mapped_column(JSON, default=list)
    architecture: Mapped[str] = mapped_column(Text, nullable=True)
    resume_bullet: Mapped[str] = mapped_column(Text, nullable=True)



class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    skill_id: Mapped[str] = mapped_column(String(36), ForeignKey("skills.id"), nullable=True)
    skill_name: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(500))
    questions: Mapped[list] = mapped_column(JSON, default=list)
    passing_score: Mapped[float] = mapped_column(Float, default=70.0)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=15)


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    assessment_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessments.id"))
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    skill_estimate: Mapped[float] = mapped_column(Float, default=0.0)
    feedback: Mapped[str] = mapped_column(Text, nullable=True)


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    total_weeks: Mapped[int] = mapped_column(Integer, default=0)
    phases: Mapped[list] = mapped_column(JSON, default=list)
    milestones: Mapped[list] = mapped_column(JSON, default=list)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    roadmap_id: Mapped[str] = mapped_column(String(36), ForeignKey("roadmaps.id"), index=True)
    resource_id: Mapped[str] = mapped_column(String(36), nullable=True)
    project_id: Mapped[str] = mapped_column(String(36), nullable=True)
    phase_number: Mapped[int] = mapped_column(Integer)
    step_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(30), default="not_started")
    order: Mapped[int] = mapped_column(Integer, default=0)


class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    resource_id: Mapped[str] = mapped_column(String(36), nullable=True)
    project_id: Mapped[str] = mapped_column(String(36), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="not_started")
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    time_spent_hours: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes: Mapped[str] = mapped_column(Text, nullable=True)


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    resource_id: Mapped[str] = mapped_column(String(36), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, default=3)
    helpful: Mapped[bool] = mapped_column(Boolean, default=True)
    reason: Mapped[str] = mapped_column(String(100), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(500), default="New Conversation")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("chat_sessions.id"), index=True)
    role: Mapped[str] = mapped_column(String(20))  # user/assistant
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)

    session = relationship("ChatSession", back_populates="messages")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    resource_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_resources.id"))
    score: Mapped[float] = mapped_column(Float, default=0.0)
    explanation: Mapped[str] = mapped_column(Text, nullable=True)
    goal_relevance: Mapped[float] = mapped_column(Float, default=0.0)
    skill_gap_relevance: Mapped[float] = mapped_column(Float, default=0.0)
    prerequisite_fit: Mapped[float] = mapped_column(Float, default=0.0)
    difficulty_fit: Mapped[float] = mapped_column(Float, default=0.0)
    time_fit: Mapped[float] = mapped_column(Float, default=0.0)
    preference_fit: Mapped[float] = mapped_column(Float, default=0.0)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
