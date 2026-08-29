"""
Groq AI Provider — Uses Llama 3 via Groq (free tier).
Free tier: ~30 RPM, 14,400 RPD as of 2024.
Falls back to DemoProvider on any error.
"""
import json
import re
from typing import Dict, List, Any

from backend.app.ai.base import BaseAIProvider
from backend.app.config.settings import settings


class GroqProvider(BaseAIProvider):
    """Groq Llama3 provider (free tier)."""

    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        if not settings.AI_API_KEY:
            return
        try:
            from groq import Groq
            self.client = Groq(api_key=settings.AI_API_KEY)
        except Exception as e:
            print(f"[GroqProvider] Failed to initialize: {e}")

    async def _generate(self, system: str, user: str) -> str:
        if not self.client:
            raise RuntimeError("Groq client not initialized")
        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=512,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Groq generation failed: {e}")

    async def extract_profile(self, user_input: str) -> Dict[str, Any]:
        system = "You are a profile extractor. Return ONLY valid JSON with keys: target_role, experience_level, weekly_hours, current_skills (dict), career_goal."
        try:
            text = await self._generate(system, user_input)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        from backend.app.ai.demo_provider import DemoProvider
        return await DemoProvider().extract_profile(user_input)

    async def generate_explanation(self, context: Dict[str, Any]) -> str:
        system = "You are an AI learning mentor. Generate concise, specific explanations for resource recommendations. Use markdown. Max 100 words."
        user = f"Resource: {context.get('resource', {}).get('title', 'Resource')}. Goal: {context.get('profile', {}).get('target_role', 'role')}. Explain why this is recommended."
        try:
            return await self._generate(system, user)
        except Exception:
            from backend.app.ai.demo_provider import DemoProvider
            return await DemoProvider().generate_explanation(context)

    async def chat(self, messages: List[Dict], context: Dict[str, Any]) -> str:
        from backend.app.ai.base import format_learner_context

        system = f"""You are Skillora's AI Mentor: a friendly personal study companion for tech learners.

Learner context:
{format_learner_context(context)}

Rules:
- Match the user's language. English -> English, Hindi -> Hindi, Hinglish -> natural Hinglish.
- Use their goal and gaps when relevant.
- Be concise, practical, and friendly.
- Do not fabricate completed courses, scores, certificates, or progress.
- For concepts, include a simple explanation, analogy, small example, and quick recap.
- Keep responses under 250 words unless the user asks for detail."""
        last_msg = "\n".join(
            f"{'User' if m.get('role') == 'user' else 'Mentor'}: {m.get('content', '')}"
            for m in messages[-8:]
        ) or "Hello"
        try:
            return await self._generate(system, last_msg)
        except Exception:
            from backend.app.ai.demo_provider import DemoProvider
            return await DemoProvider().chat(messages, context)

    async def interpret_feedback(self, feedback: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system = "Interpret learner feedback. Return JSON: {action, reason, message}. Actions: increase_difficulty/add_prerequisites/reduce_weekly_hours/acknowledge"
        try:
            text = await self._generate(system, feedback)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        from backend.app.ai.demo_provider import DemoProvider
        return await DemoProvider().interpret_feedback(feedback, context)
