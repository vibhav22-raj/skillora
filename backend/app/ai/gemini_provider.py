"""
Google Gemini AI Provider — Uses Gemini 1.5 Flash (free tier).
Free tier: 15 RPM, 1M TPM, 1500 RPD as of 2024.
Falls back to DemoProvider on any error.
"""
import json
import re
from typing import Dict, List, Any

from app.ai.base import BaseAIProvider
from app.config.settings import settings


class GeminiProvider(BaseAIProvider):
    """Google Gemini 1.5 Flash provider."""

    def __init__(self):
        self.model = None
        self._init_model()

    def _init_model(self):
        """Initialize Gemini model if API key is available."""
        if not settings.AI_API_KEY:
            return
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.AI_API_KEY)
            self.model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024,
                },
            )
        except Exception as e:
            print(f"[GeminiProvider] Failed to initialize: {e}")
            self.model = None

    async def _generate(self, prompt: str) -> str:
        """Generate text with Gemini, with error handling."""
        if not self.model:
            raise RuntimeError("Gemini model not initialized")
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}")

    async def extract_profile(self, user_input: str) -> Dict[str, Any]:
        prompt = f"""Extract structured profile information from this text. Return ONLY valid JSON.

Text: "{user_input}"

Return this exact JSON structure:
{{
  "target_role": "one of: AI/ML Engineer, Data Scientist, Data Analyst, Software Engineer, Frontend Developer, Backend Developer, Full Stack Developer, Cloud Engineer, DevOps Engineer, Cybersecurity Analyst",
  "experience_level": "beginner or intermediate or advanced",
  "weekly_hours": <number>,
  "current_skills": {{"Python": 3, "SQL": 2}},
  "career_goal": "brief description"
}}"""
        try:
            text = await self._generate(prompt)
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        # Fallback to demo
        from app.ai.demo_provider import DemoProvider
        return await DemoProvider().extract_profile(user_input)

    async def generate_explanation(self, context: Dict[str, Any]) -> str:
        resource = context.get("resource", {})
        profile = context.get("profile", {})
        skill_gaps = context.get("skill_gaps", [])

        top_gaps = skill_gaps[:3]
        gaps_str = json.dumps(top_gaps, indent=2)

        prompt = f"""You are an AI learning mentor. Explain why this resource is recommended for this learner.
Be specific, concise, and encouraging. Use markdown. Max 100 words.

Resource: {resource.get('title', 'Resource')} (Skills: {', '.join(resource.get('skills', []))})
Learner goal: {profile.get('target_role', 'Software Engineer')}
Top skill gaps: {gaps_str}

Explain why this resource specifically helps close their skill gaps and advances their goal."""
        try:
            return await self._generate(prompt)
        except Exception:
            from app.ai.demo_provider import DemoProvider
            return await DemoProvider().generate_explanation(context)

    async def chat(self, messages: List[Dict], context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        skill_gaps = context.get("skill_gaps", [])
        top_gaps_str = ', '.join(g['skill_name'] for g in skill_gaps[:3]) if skill_gaps else 'various skills'

        system_context = f"""You are LearnPath AI Mentor — a friendly, knowledgeable personal study companion for tech learners.

LEARNER PROFILE:
- Target role: {profile.get('target_role', 'Software Engineer')}
- Experience: {profile.get('experience_level', 'intermediate')}
- Weekly hours available: {profile.get('weekly_hours', 10)}h
- Top skill gaps: {top_gaps_str}

PERSONALITY:
- Be warm and encouraging like a helpful senior colleague or study buddy
- Patient, never condescending
- Celebrate progress, not just results
- Be concise — no unnecessary essays unless explicitly asked

LANGUAGE (CRITICAL):
- Detect the language of the user's message
- If they write in Hindi (Devanagari) → respond fully in Hindi
- If they write in Hinglish (romanized Hindi mixed with English) → respond in natural Hinglish
- If they write in English → respond in English
- Never force the user to write in English
- Indian learners often mix languages — match their style

EXPLANATION STYLE (for technical concepts):
1. Simple one-line summary
2. Real-world analogy (preferably relatable to Indian context)
3. Small concrete example or code snippet
4. Key rules or pitfalls
5. Quick recap

CONTEXT RULES:
- Never fabricate progress, scores, course completions, or certificates
- If unsure about user's progress, say so clearly
- Always reference their specific goal and role when relevant
- Stay focused on tech learning: CS, AI/ML, data science, web dev, career, projects, DSA, interviews

Use markdown formatting. Keep responses under 300 words unless a detailed explanation is explicitly needed."""

        conversation = "\n".join([
            f"{'User' if m['role'] == 'user' else 'Mentor'}: {m['content']}"
            for m in messages[-8:]  # Last 8 messages for context
        ])

        prompt = f"{system_context}\n\nConversation:\n{conversation}\n\nMentor:"
        try:
            return await self._generate(prompt)
        except Exception:
            from app.ai.demo_provider import DemoProvider
            return await DemoProvider().chat(messages, context)


    async def interpret_feedback(self, feedback: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Interpret this learner feedback and suggest a roadmap adaptation.
Return ONLY valid JSON.

Feedback: "{feedback}"

Return: {{"action": "one of: increase_difficulty/add_prerequisites/reduce_weekly_hours/increase_weekly_hours/refilter_recommendations/acknowledge", "reason": "...", "message": "...", "adjustment": "..."}}"""
        try:
            text = await self._generate(prompt)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        from app.ai.demo_provider import DemoProvider
        return await DemoProvider().interpret_feedback(feedback, context)
