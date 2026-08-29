"""Abstract base class for all AI providers."""
from abc import ABC, abstractmethod
from typing import Dict, List, Any


def format_learner_context(context: Dict[str, Any]) -> str:
    """Compact learner snapshot for mentor prompts. Deterministic, no extra LLM calls."""
    profile = context.get("profile") or {}
    skill_gaps = context.get("skill_gaps") or []
    roadmap = context.get("roadmap") or {}
    milestone = context.get("current_milestone")
    latest = context.get("latest_assessment")
    top_gaps = ", ".join(g.get("skill_name", "") for g in skill_gaps[:3]) or "core skills"
    milestone_title = ""
    if isinstance(milestone, dict):
        milestone_title = milestone.get("title") or milestone.get("description") or ""
    latest_line = "none yet"
    if latest:
        latest_line = f"score {latest.get('score', 0):.0f}% ({'passed' if latest.get('passed') else 'not passed'})"
    return (
        f"- Target role: {profile.get('target_role', 'Software Engineer')}\n"
        f"- Career goal: {profile.get('career_goal') or 'not set'}\n"
        f"- Experience: {profile.get('experience_level', 'intermediate')}\n"
        f"- Weekly hours: {profile.get('weekly_hours', 10)}\n"
        f"- Learning style: {profile.get('learning_style') or 'mixed'}\n"
        f"- Top skill gaps: {top_gaps}\n"
        f"- Roadmap: {roadmap.get('title') or 'not generated'} ({roadmap.get('total_weeks') or 0} weeks)\n"
        f"- Current phase: {roadmap.get('current_phase') or 'not started'}\n"
        f"- Current milestone: {milestone_title or 'not set'}\n"
        f"- Latest assessment: {latest_line}"
    )


class BaseAIProvider(ABC):
    """Base interface that all AI providers must implement."""

    @abstractmethod
    async def extract_profile(self, user_input: str) -> Dict[str, Any]:
        """
        Extract structured profile data from natural language input.
        Returns: {target_role, experience_level, weekly_hours, current_skills, career_goal}
        """
        ...

    @abstractmethod
    async def generate_explanation(self, context: Dict[str, Any]) -> str:
        """
        Generate a contextual explanation for a recommendation.
        Context includes: resource, profile, skill_gaps
        Returns: markdown-formatted explanation string
        """
        ...

    @abstractmethod
    async def chat(self, messages: List[Dict], context: Dict[str, Any]) -> str:
        """
        Generate a mentor chat response.
        Messages: list of {role: 'user'|'assistant', content: str}
        Context: {profile, skill_gaps, roadmap, progress}
        Returns: markdown-formatted response string
        """
        ...

    @abstractmethod
    async def interpret_feedback(self, feedback: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpret user feedback and determine appropriate roadmap adaptation.
        Returns: {action, reason, message, adjustment_params}
        """
        ...
