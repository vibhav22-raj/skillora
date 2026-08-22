import os

base_dir = r"F:\github clone rep\HCL_Amplified\backend\app\ai"

base = """from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    @abstractmethod
    async def extract_profile(self, user_input: str) -> dict: ...
    
    @abstractmethod
    async def generate_explanation(self, context: dict) -> str: ...
    
    @abstractmethod
    async def chat(self, messages: list, context: dict) -> str: ...
    
    @abstractmethod
    async def interpret_feedback(self, feedback: str, context: dict) -> dict: ...
"""
with open(os.path.join(base_dir, "base.py"), "w") as f:
    f.write(base)

demo = """from .base import BaseAIProvider

class DemoProvider(BaseAIProvider):
    async def extract_profile(self, user_input: str) -> dict:
        return {"target_role": "AI/ML Engineer", "experience_level": "beginner"}
        
    async def generate_explanation(self, context: dict) -> str:
        return "This is a highly recommended resource based on your goal."
        
    async def chat(self, messages: list, context: dict) -> str:
        return "Hello! I am your AI learning assistant. How can I help you today?"
        
    async def interpret_feedback(self, feedback: str, context: dict) -> dict:
        return {"action": "adapt_roadmap", "reason": feedback}
"""
with open(os.path.join(base_dir, "demo_provider.py"), "w") as f:
    f.write(demo)

gemini = """from .base import BaseAIProvider
import google.generativeai as genai
from app.config.settings import settings

if settings.AI_API_KEY:
    genai.configure(api_key=settings.AI_API_KEY)

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash') if settings.AI_API_KEY else None
        
    async def extract_profile(self, user_input: str) -> dict:
        if not self.model: return {"target_role": "Unknown"}
        return {"target_role": "AI/ML Engineer", "experience_level": "beginner"}
        
    async def generate_explanation(self, context: dict) -> str:
        if not self.model: return "Demo explanation"
        return "Explanation based on context"
        
    async def chat(self, messages: list, context: dict) -> str:
        if not self.model: return "Demo chat"
        return "Gemini response"
        
    async def interpret_feedback(self, feedback: str, context: dict) -> dict:
        return {"action": "adapt"}
"""
with open(os.path.join(base_dir, "gemini_provider.py"), "w") as f:
    f.write(gemini)

factory = """from .demo_provider import DemoProvider
from .gemini_provider import GeminiProvider
from app.config.settings import settings

def get_ai_provider():
    if settings.AI_PROVIDER == 'gemini':
        return GeminiProvider()
    return DemoProvider()
"""
with open(os.path.join(base_dir, "provider_factory.py"), "w") as f:
    f.write(factory)
    
print("AI complete.")
