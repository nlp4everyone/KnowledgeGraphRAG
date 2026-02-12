# Typing
from typing import Optional
# Config
from src.core.config import OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GROQ_API_KEY
from graphiti_core.llm_client.client import LLMConfig, LLMClient
# Schemas
from src.schemas.llm.provider import Provider
from src.services.llm.factory import LLMClientFactory, ProviderType
from src.utils.config_loader.toml_loader import TomlConfigLoader
# Chat model
from langchain_core.language_models.chat_models import BaseChatModel

# Define loader
config_loader = TomlConfigLoader()
# API key mapping
api_keys = {Provider.OPENAI: OPENAI_API_KEY,
            Provider.ANTHROPIC: ANTHROPIC_API_KEY,
            Provider.GEMINI: GEMINI_API_KEY,
            Provider.GROQ: GROQ_API_KEY}

def get_graphiti_client(provider: ProviderType,
                        model: Optional[str] = None,        # None = use default from config
                        max_tokens: Optional[int] = None,    # None = use default from config
                        temperature: Optional[float] = None, # None = use default from config
                        **kwargs) -> LLMClient:
    """Get LLM client based on provider and optional parameters.
    
    Args:
        provider: LLM provider (OPENAI, ANTHROPIC, GEMINI, GROQ)
        model: Model name. If None, uses default from config
        max_tokens: Max tokens. If None, uses default from config
        temperature: Temperature. If None, uses default from config
        **kwargs: Additional LLM config parameters
    
    Returns:
        Configured LLM client instance
    """
    llm_config = config_loader.get_llm_config()

    # Check provider
    if provider not in api_keys:
        raise ValueError(f"Provider '{provider}' not supported")

    # Define api key
    api_key = api_keys[provider]
    # Raise exception
    if not api_key:
        raise ValueError(f"API key for {provider.capitalize()} not found in environment variables")

    # Load defaults from config if not specified
    provider_key = provider.value.lower()
    provider_config = llm_config.get("llm_providers", {}).get(provider_key, {})
    
    if model is None:
        if "default_model" not in provider_config:
            raise ValueError(f"No default model configured for provider '{provider}' in llm_config.toml")
        model = provider_config["default_model"]
    
    if max_tokens is None:
        max_tokens = provider_config.get("max_tokens")
    
    if temperature is None:
        temperature = provider_config.get("temperature")

    # Config
    config = LLMConfig(api_key=api_key,
                       model=model,
                       max_tokens=max_tokens,
                       temperature=temperature,
                       **kwargs)
    # Return
    return LLMClientFactory.create_client(provider, config)

def get_langchain_client(provider: ProviderType,
                         model: Optional[str] = None,        # None = use default from config
                         temperature: Optional[float] = None, # None = use default from config
                         max_tokens: Optional[int] = None,    # None = use default from config
                         **kwargs) -> BaseChatModel:
    """Get LangChain client based on provider and optional parameters.
    
    Args:
        provider: LLM provider (OPENAI, ANTHROPIC, GEMINI, GROQ)
        model: Model name. If None, uses default from config
        temperature: Temperature. If None, uses default from config
        max_tokens: Max tokens. If None, uses default from config
        **kwargs: Additional LangChain parameters
    
    Returns:
        Configured LangChain client instance
    """
    llm_config = config_loader.get_llm_config()

    # Check provider
    if provider not in api_keys:
        raise ValueError(f"Provider '{provider}' not supported")

    # Define api key
    api_key = api_keys[provider]
    # Raise exception
    if not api_key:
        raise ValueError(f"API key for {provider.capitalize()} not found in environment variables")

    # Load defaults from config if not specified
    provider_key = provider.value.lower()
    provider_config = llm_config.get("llm_providers", {}).get(provider_key, {})
    
    if model is None:
        if "default_model" not in provider_config:
            raise ValueError(f"No default model configured for provider '{provider}' in llm_config.toml")
        model = provider_config["default_model"]
    
    if max_tokens is None:
        max_tokens = provider_config.get("max_tokens")
    
    if temperature is None:
        temperature = provider_config.get("temperature")

    # Return LangChain client from factory
    return LLMClientFactory.create_langchain_client(provider=provider,
                                                    api_key=api_key,
                                                    model=model,
                                                    temperature=temperature,
                                                    max_tokens=max_tokens,
                                                    **kwargs)
