from strenum import StrEnum

class Provider(StrEnum):
    """Supported LLM providers"""
    
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    GROQ = "groq"
    
    @classmethod
    def get_all_providers(cls) -> list[str]:
        """Get list of all supported providers"""
        return [provider.value for provider in cls]
    
    @classmethod
    def is_supported(cls, provider: str) -> bool:
        """Check if a provider is supported"""
        return provider.lower() in [p.value for p in cls]
