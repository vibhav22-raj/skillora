"""
Groq AI Provider — Uses Llama 3.3 / 3.1 via Groq.
Primary: llama-3.3-70b-versatile
Fast fallback: llama-3.1-8b-instant
Final fallback: DemoProvider
"""
import json
import re
from typing import Dict, List, Any

try:
    from backend.app.ai.base import BaseAIProvider, format_learner_context
    from backend.app.config.settings import settings
except ImportError:
    from app.ai.base import BaseAIProvider, format_learner_context
    from app.config.settings import settings


class GroqProvider(BaseAIProvider):
    """Groq Llama provider with primary 70B and fast 8B fallback."""

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

    async def _generate(self, system: str, user: str, max_tokens: int = 512) -> str:
        if not self.client:
            raise RuntimeError("Groq client not initialized")
        
        # Primary: llama-3.3-70b-versatile, fallback: llama-3.1-8b-instant, then available high-performance Groq models
        models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b",
            "groq/compound",
        ]
        for model_name in models:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"[GroqProvider] Model {model_name} warning: {e}")
                continue
        raise RuntimeError("All Groq models failed")

    async def extract_profile(self, user_input: str) -> Dict[str, Any]:
        system = "You are a profile extractor for Skillora. Return ONLY valid JSON with keys: target_role, experience_level, weekly_hours, current_skills (dict of skill: level 1-5), career_goal."
        try:
            text = await self._generate(system, user_input)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        try:
            from backend.app.ai.demo_provider import DemoProvider
        except ImportError:
            from app.ai.demo_provider import DemoProvider
        return await DemoProvider().extract_profile(user_input)

    async def generate_explanation(self, context: Dict[str, Any]) -> str:
        system = "You are Skillora's AI learning mentor. Generate concise, specific explanations for resource recommendations. Use markdown. Max 120 words. Be specific about why this resource fits the learner's gap, format, and duration."
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
            try:
                from backend.app.ai.demo_provider import DemoProvider
            except ImportError:
                from app.ai.demo_provider import DemoProvider
            return await DemoProvider().generate_explanation(context)

    async def chat(self, messages: List[Dict], context: Dict[str, Any]) -> str:
        system = f"""You are Skillora's AI Mentor: a friendly personal study companion for tech learners.

Learner context:
{format_learner_context(context)}

Rules:
- Match the user's language. English -> English, Hindi -> Hindi, Hinglish -> natural Hinglish.
- Explicitly reference their target goal, skill gaps, current roadmap milestone, and recent assessments when helpful.
- Be concise, practical, and action-oriented.
- Do not fabricate completed courses, scores, certificates, or progress.
- If they have limited time (e.g. 30 mins), suggest high-impact micro-learning or quick problem-solving.
- If they are struggling, provide intuition, small analogies, code snippets, and encouragement.
- Keep responses under 250 words unless detailed depth is requested."""
        
        last_msg = "\n".join(
            f"{'User' if m.get('role') == 'user' else 'Mentor'}: {m.get('content', '')}"
            for m in messages[-8:]
        ) or "Hello"
        try:
            return await self._generate(system, last_msg, max_tokens=600)
        except Exception:
            try:
                from backend.app.ai.demo_provider import DemoProvider
            except ImportError:
                from app.ai.demo_provider import DemoProvider
            return await DemoProvider().chat(messages, context)

    async def interpret_feedback(self, feedback: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system = "Interpret learner feedback for Skillora. Return JSON: {action, reason, message}. Actions: increase_difficulty/add_prerequisites/reduce_weekly_hours/acknowledge"
        try:
            text = await self._generate(system, feedback)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        try:
            from backend.app.ai.demo_provider import DemoProvider
        except ImportError:
            from app.ai.demo_provider import DemoProvider
        return await DemoProvider().interpret_feedback(feedback, context)

