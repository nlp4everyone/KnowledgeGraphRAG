# Typing
from typing import Literal, Optional
# Provider
from src.schemas.llm.provider import Provider
# Client
from graphiti_core.llm_client.gemini_client import GeminiClient
from graphiti_core.llm_client.anthropic_client import AnthropicClient
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.llm_client.groq_client import GroqClient
# Other
from graphiti_core.llm_client.client import LLMClient, LLMConfig
# LangChain
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel

ProviderType = Literal[Provider.OPENAI, Provider.ANTHROPIC, Provider.GEMINI, Provider.GROQ]

class LLMClientFactory:
    """Factory for creating LLM clients"""
    @staticmethod
    def create_client(provider: ProviderType,
                      config: LLMConfig) -> LLMClient:
        """Create an LLM client for the specified provider"""
        
        if provider == Provider.GEMINI:
            return GeminiClient(config = config)
        elif provider == Provider.ANTHROPIC:
            return AnthropicClient(config = config)
        elif provider == Provider.GROQ:
            return GroqClient(config = config)
        elif provider == Provider.OPENAI:
            return OpenAIClient(config = config,
                                max_tokens = config.max_tokens)
            # raise NotImplementedError("Graphiti not fully supports OpenAI")
        else:
            raise ValueError(f"Provider '{provider}' not supported yet.")
    
    @staticmethod
    def get_supported_providers() -> list[str]:
        """Get list of supported providers"""
        return Provider.get_all_providers()
    
    @staticmethod
    def create_langchain_client(provider: ProviderType,
                                api_key: str,
                                model: str,
                                temperature: float,
                                max_tokens: int,
                                **kwargs) -> BaseChatModel:
        """Create a LangChain client for the specified provider"""
        
        if provider == Provider.OPENAI:
            return ChatOpenAI(model = model,
                              temperature = temperature,
                              max_tokens = max_tokens,
                              api_key = api_key,
                              **kwargs)
        elif provider == Provider.ANTHROPIC:
            return ChatAnthropic(model = model,
                                 temperature = temperature,
                                 max_tokens = max_tokens,
                                 anthropic_api_key = api_key,
                                 **kwargs)
        elif provider == Provider.GEMINI:
            return ChatGoogleGenerativeAI(model = model,
                                          temperature = temperature,
                                          max_tokens = max_tokens,
                                          api_key = api_key,
                                          **kwargs)
        elif provider == Provider.GROQ:
            return ChatGroq(model = model,
                            temperature = temperature,
                            max_tokens = max_tokens,
                            **kwargs)
        else:
            raise ValueError(f"Provider '{provider}' not supported for LangChain client.")
