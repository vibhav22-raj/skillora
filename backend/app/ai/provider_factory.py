"""
AI Provider Factory — Returns Groq provider with Demo fallback.
Chain: groq_provider -> demo_provider
"""
from typing import Optional

try:
    from backend.app.ai.base import BaseAIProvider
    from backend.app.config.settings import settings
except ImportError:
    from app.ai.base import BaseAIProvider
    from app.config.settings import settings

_provider_instance: Optional[BaseAIProvider] = None


def get_ai_provider() -> BaseAIProvider:
    """
    Return AI provider based on settings.AI_PROVIDER.
    Falls back to DemoProvider if Groq fails or API key is absent.
    """
    global _provider_instance

    if _provider_instance is not None:
        return _provider_instance

    provider_name = (settings.AI_PROVIDER or "groq").lower()

    if provider_name == "groq" and settings.AI_API_KEY:
        try:
            try:
                from backend.app.ai.groq_provider import GroqProvider
            except ImportError:
                from app.ai.groq_provider import GroqProvider
            provider = GroqProvider()
            if provider.client:
                _provider_instance = provider
                return _provider_instance
        except Exception as e:
            print(f"[ProviderFactory] Groq init failed: {e}. Falling back to DemoProvider.")

    # Final offline fallback
    try:
        from backend.app.ai.demo_provider import DemoProvider
    except ImportError:
        from app.ai.demo_provider import DemoProvider
    _provider_instance = DemoProvider()
    print("[ProviderFactory] Using DemoProvider (offline/deterministic)")
    return _provider_instance


def reset_provider():
    """Reset cached provider (useful for testing)."""
    global _provider_instance
    _provider_instance = None
