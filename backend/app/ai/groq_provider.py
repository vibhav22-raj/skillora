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
                    temperature=0.6,
                )
                if response.choices and response.choices[0].message.content:
                    content = response.choices[0].message.content.strip()
                    # Markdown fence balancing: ensure code blocks are never left unclosed
                    if content.count("```") % 2 != 0:
                        content += "\n```"
                    return content
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
        system = (
            "You are Skillora's AI learning mentor. Generate a concise, explainable 1-2 sentence recommendation reason. "
            "Follow this pattern: 'Recommended because you are targeting [Goal] and currently have a [Priority] priority gap in [Skill]. This [Format] directly bridges that gap at your level.' "
            "Keep it strictly under 45 words. Be direct, clear, and personalized."
        )
        resource = context.get('resource', {}) or {}
        profile = context.get('profile', {}) or {}
        skill_gaps = context.get('skill_gaps', []) or []
        top_gap = skill_gaps[0].get('skill_name') if skill_gaps else 'Core Skills'
        gap_priority = skill_gaps[0].get('priority', 'high') if skill_gaps else 'high'
        user = f"Resource: {resource.get('title')}, Provider: {resource.get('provider')}, Format: {resource.get('format')}, Learner Goal: {profile.get('target_role')}, Top Gap: {top_gap} ({gap_priority} priority)."
        try:
            return await self._generate(system, user)
        except Exception:
            try:
                from backend.app.ai.demo_provider import DemoProvider
            except ImportError:
                from app.ai.demo_provider import DemoProvider
            return await DemoProvider().generate_explanation(context)

    async def chat(self, messages: List[Dict], context: Dict[str, Any]) -> str:
        system = f"""You are Skillora's AI Mentor: a personalized learning coach for this student.

Learner Context:
{format_learner_context(context)}

CRITICAL RESPONSE RULES:
1. ALWAYS provide a COMPLETE, self-contained response. Never trail off or leave code unclosed.
2. For educational concept questions (e.g. "What is X?"), strictly use this concise 3-part structure:
   **Definition**
   Clear, simple explanation in 2-4 sentences matched to their level.

   **Basic Example**
   ONE small, beginner-friendly example (a tiny 2-4 line code snippet or conceptual analogy).

   **Why it matters**
   2-3 concise bullet points explaining practical relevance to modern software development or their target path.

3. STRICT PROHIBITIONS for basic questions:
   - Do NOT generate giant PyTorch/TensorFlow implementations.
   - Do NOT write multi-page lectures, giant tables, or unrequested 20-hr study plans.
   - Keep total length concise (~100 to 180 words).

4. Match the user's language (English -> English, Hindi -> Hindi, Hinglish -> Hinglish)."""
        
        last_msg = "\n".join(
            f"{'User' if m.get('role') == 'user' else 'Mentor'}: {m.get('content', '')}"
            for m in messages[-8:]
        ) or "Hello"
        try:
            return await self._generate(system, last_msg, max_tokens=1024)
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

