import os

base_dir = r"F:\github clone rep\HCL_Amplified\backend\app"

db_base = """from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
"""
with open(os.path.join(base_dir, "database", "base.py"), "w") as f:
    f.write(db_base)


models = """from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
import uuid
from app.database.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    profile = relationship("LearnerProfile", back_populates="user", uselist=False)

class LearnerProfile(Base):
    __tablename__ = 'learner_profiles'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    target_role: Mapped[str] = mapped_column(String, nullable=True)
    experience_level: Mapped[str] = mapped_column(String, nullable=True)
    education: Mapped[str] = mapped_column(String, nullable=True)
    career_goal: Mapped[str] = mapped_column(String, nullable=True)
    weekly_hours: Mapped[float] = mapped_column(Float, nullable=True)
    learning_style: Mapped[str] = mapped_column(String, nullable=True)
    target_deadline: Mapped[str] = mapped_column(String, nullable=True)  # Use string for simple date in sqlite
    preferred_duration: Mapped[str] = mapped_column(String, nullable=True)
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    weaknesses: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="profile")

class Skill(Base):
    __tablename__ = 'skills'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer)
    prerequisites: Mapped[list] = mapped_column(JSON, default=list)
    tags: Mapped[list] = mapped_column(JSON, default=list)

class UserSkill(Base):
    __tablename__ = 'user_skills'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    skill_id: Mapped[str] = mapped_column(String, ForeignKey('skills.id'))
    current_level: Mapped[int] = mapped_column(Integer, default=0)
    target_level: Mapped[int] = mapped_column(Integer, default=0)
    gap_score: Mapped[float] = mapped_column(Float, default=0.0)
    priority: Mapped[str] = mapped_column(String, default="low")
    last_assessed: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class LearningResource(Base):
    __tablename__ = 'learning_resources'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    provider: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String, nullable=True)
    skills: Mapped[list] = mapped_column(JSON, default=list)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    duration_hours: Mapped[float] = mapped_column(Float, default=1.0)
    format: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)
    prerequisites: Mapped[list] = mapped_column(JSON, default=list)

class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    skills: Mapped[list] = mapped_column(JSON, default=list)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    duration_hours: Mapped[float] = mapped_column(Float, default=1.0)
    category: Mapped[str] = mapped_column(String, nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    github_template_url: Mapped[str] = mapped_column(String, nullable=True)

class Assessment(Base):
    __tablename__ = 'assessments'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    skill_id: Mapped[str] = mapped_column(String, ForeignKey('skills.id'))
    title: Mapped[str] = mapped_column(String)
    questions: Mapped[list] = mapped_column(JSON, default=list)
    passing_score: Mapped[float] = mapped_column(Float, default=70.0)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=30)

class AssessmentAttempt(Base):
    __tablename__ = 'assessment_attempts'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    assessment_id: Mapped[str] = mapped_column(String, ForeignKey('assessments.id'))
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    skill_estimate: Mapped[float] = mapped_column(Float, default=0.0)
    feedback: Mapped[str] = mapped_column(String, nullable=True)

class Roadmap(Base):
    __tablename__ = 'roadmaps'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    total_weeks: Mapped[int] = mapped_column(Integer, default=0)
    phases: Mapped[list] = mapped_column(JSON, default=list)
    milestones: Mapped[list] = mapped_column(JSON, default=list)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class RoadmapStep(Base):
    __tablename__ = 'roadmap_steps'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    roadmap_id: Mapped[str] = mapped_column(String, ForeignKey('roadmaps.id'))
    resource_id: Mapped[str] = mapped_column(String, nullable=True)
    project_id: Mapped[str] = mapped_column(String, nullable=True)
    phase_number: Mapped[int] = mapped_column(Integer)
    step_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String, default="not_started")
    order: Mapped[int] = mapped_column(Integer, default=0)

class Progress(Base):
    __tablename__ = 'progress'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    resource_id: Mapped[str] = mapped_column(String, nullable=True)
    project_id: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="not_started")
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    time_spent_hours: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes: Mapped[str] = mapped_column(String, nullable=True)

class Feedback(Base):
    __tablename__ = 'feedback'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    resource_id: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    helpful: Mapped[bool] = mapped_column(Boolean)
    reason: Mapped[str] = mapped_column(String, nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String, ForeignKey('chat_sessions.id'))
    role: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)

class Recommendation(Base):
    __tablename__ = 'recommendations'
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    resource_id: Mapped[str] = mapped_column(String, ForeignKey('learning_resources.id'))
    score: Mapped[float] = mapped_column(Float, default=0.0)
    explanation: Mapped[str] = mapped_column(String, nullable=True)
    goal_relevance: Mapped[float] = mapped_column(Float, default=0.0)
    skill_gap_relevance: Mapped[float] = mapped_column(Float, default=0.0)
    prerequisite_fit: Mapped[float] = mapped_column(Float, default=0.0)
    difficulty_fit: Mapped[float] = mapped_column(Float, default=0.0)
    time_fit: Mapped[float] = mapped_column(Float, default=0.0)
    preference_fit: Mapped[float] = mapped_column(Float, default=0.0)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
"""
with open(os.path.join(base_dir, "models", "__init__.py"), "w") as f:
    f.write(models)
    
schemas = """from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any
from datetime import datetime

# Common response wrapper
class ApiResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: str = ""

# Auth schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    is_demo: bool
    
    class Config:
        from_attributes = True

# Profile schemas
class ProfileUpdate(BaseModel):
    target_role: Optional[str] = None
    experience_level: Optional[str] = None
    education: Optional[str] = None
    career_goal: Optional[str] = None
    weekly_hours: Optional[float] = None
    learning_style: Optional[str] = None
    target_deadline: Optional[str] = None
    preferred_duration: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None

class ProfileOnboarding(BaseModel):
    user_input: str

# Recommendation schemas
class RecommendationResponse(BaseModel):
    id: str
    resource_id: str
    score: float
    explanation: Optional[str]
    goal_relevance: float
    skill_gap_relevance: float
    prerequisite_fit: float
    difficulty_fit: float
    time_fit: float
    preference_fit: float
    
    class Config:
        from_attributes = True

# Skill schemas
class SkillUpdate(BaseModel):
    level: int
    
class SkillGapResponse(BaseModel):
    skill_name: str
    current_level: int
    target_level: int
    gap: int
    priority: str
    recommended_resources: List[str]

# Chat schemas
class ChatMessageReq(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatSessionCreate(BaseModel):
    title: str

# Progress schemas
class ProgressUpdate(BaseModel):
    status: str
    completion_percentage: float
    time_spent_hours: float
    notes: Optional[str] = None

# Assessments
class AssessmentSubmit(BaseModel):
    answers: dict

# Learning Path
class LearningPathAdapt(BaseModel):
    feedback: str
"""
with open(os.path.join(base_dir, "schemas", "__init__.py"), "w") as f:
    f.write(schemas)
print("Models and schemas complete.")
