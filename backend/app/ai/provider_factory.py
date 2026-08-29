"""
AI Provider Factory — Returns the configured provider with fallback chain.
Chain: configured_provider -> demo_provider
"""
from app.ai.base import BaseAIProvider
from app.config.settings import settings

_provider_instance: BaseAIProvider = None


def get_ai_provider() -> BaseAIProvider:
    """
    Return AI provider based on settings.AI_PROVIDER.
    Falls back to DemoProvider if configured provider fails.
    """
    global _provider_instance

    if _provider_instance is not None:
        return _provider_instance

    provider_name = settings.AI_PROVIDER.lower()

    if settings.DEMO_MODE or provider_name == "demo":
        from app.ai.demo_provider import DemoProvider
        _provider_instance = DemoProvider()
        return _provider_instance

    if provider_name == "gemini":
        try:
            from app.ai.gemini_provider import GeminiProvider
            provider = GeminiProvider()
            if provider.model:
                _provider_instance = provider
                return _provider_instance
        except Exception as e:
            print(f"[ProviderFactory] Gemini init failed: {e}. Falling back to Demo.")

    elif provider_name == "groq":
        try:
            from app.ai.groq_provider import GroqProvider
            provider = GroqProvider()
            if provider.client:
                _provider_instance = provider
                return _provider_instance
        except Exception as e:
            print(f"[ProviderFactory] Groq init failed: {e}. Falling back to Demo.")

    # Always fall back to demo
    from app.ai.demo_provider import DemoProvider
    _provider_instance = DemoProvider()
    print(f"[ProviderFactory] Using DemoProvider (provider={provider_name})")
    return _provider_instance


def reset_provider():
    """Reset cached provider (useful for testing)."""
    global _provider_instance
    _provider_instance = None
