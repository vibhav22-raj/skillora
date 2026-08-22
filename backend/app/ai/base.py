"""Abstract base class for all AI providers."""
from abc import ABC, abstractmethod
from typing import Dict, List, Any


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
