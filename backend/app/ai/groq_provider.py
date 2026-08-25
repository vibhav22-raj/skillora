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
        system = "You are an AI learning mentor. Generate concise, specific explanations for resource recommendations. Use markdown. Max 120 words. Be specific about why this resource fits the learner's gap, format, and duration."
        resource = context.get('resource', {}) or {}
        profile = context.get('profile', {}) or {}
        user_parts = [f"Resource: {resource.get('title', 'Resource')}"]
        if resource.get('provider'):
            user_parts.append(f"Provider: {resource.get('provider')}")
        if resource.get('format'):
            user_parts.append(f"Format: {resource.get('format')}")
        if resource.get('duration_hours'):
            user_parts.append(f"Duration: {resource.get('duration_hours')}h")
        user_parts.append(f"Learner goal: {profile.get('target_role', 'your target role')}")
        user = '. '.join(user_parts) + '. Explain concisely why this resource is recommended, referencing the learner\'s top skill gaps.'
        try:
            return await self._generate(system, user)
        except Exception:
            from backend.app.ai.demo_provider import DemoProvider
            return await DemoProvider().generate_explanation(context)

    async def chat(self, messages: List[Dict], context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        skill_gaps = context.get("skill_gaps", [])
        roadmap = context.get("roadmap")

        # Build a concise system prompt including profile, top gaps, and roadmap state
        top_gaps = ", ".join([g.get("skill_name") for g in skill_gaps[:3]]) if skill_gaps else "core skills"
        roadmap_summary = ""
        if roadmap:
            rp = roadmap
            roadmap_summary = f" Roadmap: {rp.get('title', '')}, phases: {rp.get('total_phases')}"

        system = (
            f"You are an encouraging AI learning mentor. Learner is targeting: {profile.get('target_role', 'Software Engineer')}."
            f" Top gaps: {top_gaps}.{roadmap_summary} Be concise and actionable. Use markdown. Max 150 words."
        )

        # Build user content by concatenating recent messages, while extracting explicit constraints
        last_msg = messages[-1]["content"] if messages else "Hello"
        # detect simple time constraint like '30 minutes', '1 hour', 'half hour'
        time_constraint = None
        import re
        time_patterns = [r"(\d+)\s*minutes?", r"(\d+)\s*mins?", r"(\d+)\s*hours?", r"half\s*hour", r"30\s*min"]
        for m in messages[::-1]:
            text = m.get("content", "")
            for pat in time_patterns:
                match = re.search(pat, text, re.IGNORECASE)
                if match:
                    time_constraint = match.group(0)
                    break
            if time_constraint:
                break

        # detect struggle mention
        struggle = None
        struggle_keywords = ["struggling", "difficult", "hard", "confused", "don't understand", "don't get"]
        for m in messages[::-1]:
            text = m.get("content", "").lower()
            if any(k in text for k in struggle_keywords):
                struggle = text
                break

        user_content = last_msg
        if time_constraint:
            user_content = f"[time_constraint: {time_constraint}] {user_content}"
        if struggle:
            user_content = f"[struggling_about: {struggle}] {user_content}"

        try:
            return await self._generate(system, user_content)
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
