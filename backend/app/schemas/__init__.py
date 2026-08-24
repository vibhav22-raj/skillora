"""Complete Pydantic schemas for LearnPath AI."""
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional, Any, Dict
from datetime import datetime


# ─── Common ────────────────────────────────────────────────────────────────
class ApiResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: str = ""


# ─── Auth ──────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


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

    model_config = {"from_attributes": True}


# ─── Profile ───────────────────────────────────────────────────────────────
class ProfileResponse(BaseModel):
    id: str
    user_id: str
    target_role: Optional[str] = None
    experience_level: Optional[str] = None
    education: Optional[str] = None
    career_goal: Optional[str] = None
    weekly_hours: Optional[float] = None
    learning_style: Optional[str] = None
    target_deadline: Optional[str] = None
    preferred_duration: Optional[str] = None
    strengths: List[str] = []
    weaknesses: List[str] = []
    bio: Optional[str] = None
    profile_image: Optional[str] = None  # Base64 or URL

    model_config = {"from_attributes": True}


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
    bio: Optional[str] = None
    profile_image: Optional[str] = None  # Base64 or URL



class ProfileOnboarding(BaseModel):
    """Conversational onboarding — user describes themselves in natural language."""
    goal: str
    experience_level: str
    current_skills: List[Dict[str, Any]] = []
    weekly_hours: float = 10.0
    learning_style: str = "mixed"
    target_deadline: Optional[str] = None


# ─── Skills ────────────────────────────────────────────────────────────────
class SkillResponse(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str] = None
    difficulty: int
    prerequisites: List[str] = []
    tags: List[str] = []

    model_config = {"from_attributes": True}


class UserSkillResponse(BaseModel):
    skill_id: str
    skill_name: str
    current_level: int
    target_level: int
    gap_score: float
    priority: str

    model_config = {"from_attributes": True}


class SkillUpdate(BaseModel):
    skill_name: str
    level: int


class SkillGapResponse(BaseModel):
    skill_name: str
    current_level: int
    target_level: int
    gap: int
    priority: str
    recommended_resources: List[str] = []
    description: Optional[str] = None


# ─── Resources ─────────────────────────────────────────────────────────────
class ResourceResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    provider: Optional[str] = None
    url: str
    category: Optional[str] = None
    skills: List[str] = []
    difficulty: int
    duration_hours: float
    format: Optional[str] = None
    rating: float
    tags: List[str] = []
    is_free: bool
    prerequisites: List[str] = []

    model_config = {"from_attributes": True}


# ─── Projects ──────────────────────────────────────────────────────────────
class ProjectResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    skills: List[str] = []
    difficulty: int
    duration_hours: float
    category: Optional[str] = None
    tags: List[str] = []
    github_template_url: Optional[str] = None

    model_config = {"from_attributes": True}


# ─── Recommendations ───────────────────────────────────────────────────────
class RecommendationResponse(BaseModel):
    id: str
    resource_id: str
    score: float
    explanation: Optional[str] = None
    goal_relevance: float
    skill_gap_relevance: float
    prerequisite_fit: float
    difficulty_fit: float
    time_fit: float
    preference_fit: float
    resource: Optional[ResourceResponse] = None

    model_config = {"from_attributes": True}


class FeedbackCreate(BaseModel):
    helpful: bool
    reason: Optional[str] = None  # too_easy/too_hard/not_relevant/already_known/good
    notes: Optional[str] = None


# ─── Roadmap ───────────────────────────────────────────────────────────────
class RoadmapPhase(BaseModel):
    phase_number: int
    title: str
    description: str
    weeks: int
    skills: List[str] = []
    resources: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    milestones: List[str] = []
    status: str = "not_started"
    estimated_hours: float = 0.0


class MilestoneSchema(BaseModel):
    title: str
    description: str
    skills_gained: List[str] = []
    completion_criteria: str
    phase: int


class RoadmapResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    total_weeks: int
    phases: List[Dict[str, Any]] = []
    milestones: List[Dict[str, Any]] = []
    generated_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}


class LearningPathGenerate(BaseModel):
    """Request to generate a new learning path."""
    goal: str
    free_text_goal: Optional[str] = None
    experience_level: str = "intermediate"
    current_skills: List[Dict[str, Any]] = []
    weekly_hours: float = 10.0
    learning_style: str = "mixed"
    target_deadline: Optional[str] = None


class LearningPathAdapt(BaseModel):
    """Adapt existing roadmap based on user feedback."""
    feedback: str


# ─── Assessment ────────────────────────────────────────────────────────────
class QuestionSchema(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: int  # index
    explanation: str
    type: str = "multiple_choice"


class AssessmentResponse(BaseModel):
    id: str
    skill_name: Optional[str] = None
    title: str
    questions: List[Dict[str, Any]] = []
    passing_score: float
    estimated_minutes: int

    model_config = {"from_attributes": True}


class AssessmentSubmit(BaseModel):
    answers: Dict[str, int]  # {question_id: answer_index}


class AssessmentResult(BaseModel):
    score: float
    passed: bool
    total_questions: int
    correct_answers: int
    skill_estimate: float
    feedback: str
    recommendations: List[str] = []


# ─── Chat ──────────────────────────────────────────────────────────────────
class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChatSessionCreate(BaseModel):
    title: str = "New Conversation"


# ─── Progress ──────────────────────────────────────────────────────────────
class ProgressUpdate(BaseModel):
    resource_id: Optional[str] = None
    project_id: Optional[str] = None
    status: str  # not_started/in_progress/completed/skipped
    completion_percentage: float = 0.0
    time_spent_hours: float = 0.0
    notes: Optional[str] = None


class ProgressStats(BaseModel):
    overall_completion: float
    total_resources: int
    completed_resources: int
    in_progress_resources: int
    total_hours_spent: float
    current_streak: int
    longest_streak: int
    skills_improved: int
    assessments_passed: int
    projects_completed: int


# ─── Dashboard ─────────────────────────────────────────────────────────────
class TodayTask(BaseModel):
    title: str
    type: str  # lesson/quiz/project/assessment
    estimated_minutes: int
    resource_id: Optional[str] = None
    completed: bool = False


class WeeklyActivity(BaseModel):
    day: str
    hours: float
    resources_completed: int


class NextBestAction(BaseModel):
    title: str
    description: str
    type: str
    resource_id: Optional[str] = None
    estimated_minutes: int
    reason: str


class DashboardResponse(BaseModel):
    user_name: str
    target_role: Optional[str] = None
    overall_progress: float
    current_streak: int
    hours_learned: float
    skills_improved: int
    next_best_action: Optional[NextBestAction] = None
    today_focus: List[TodayTask] = []
    skill_gaps: List[SkillGapResponse] = []
    weekly_activity: List[WeeklyActivity] = []
    current_milestone: Optional[Dict[str, Any]] = None
    recent_recommendations: List[Dict[str, Any]] = []
