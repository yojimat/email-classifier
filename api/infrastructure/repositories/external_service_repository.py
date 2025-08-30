"""
External service repository implementation.
Manages access to external service configurations following the Repository pattern.
"""
from typing import Optional
from core.interfaces.repositories import IExternalServiceRepository
from core.config import AppConfig


class ExternalServiceRepository(IExternalServiceRepository):
    """
    Concrete implementation of external service repository.
    Provides access to external service configurations and credentials.
    """

    def get_openai_api_key(self) -> Optional[str]:
        """
        Get OpenAI API key.

        Returns:
            OpenAI API key if configured, None otherwise
        """
        api_key = AppConfig.OPENAI_API_KEY
        return api_key if api_key else None

    def get_huggingface_token(self) -> Optional[str]:
        """
        Get HuggingFace token.

        Returns:
            HuggingFace token if configured, None otherwise
        """
        token = AppConfig.HUGGINGFACE_TOKEN
        return token if token else None

    def is_openai_configured(self) -> bool:
        """Check if OpenAI is properly configured"""
        return AppConfig.is_openai_configured()

    def is_huggingface_configured(self) -> bool:
        """Check if HuggingFace is properly configured"""
        return AppConfig.is_huggingface_configured()

    def get_openai_model_name(self) -> str:
        """Get OpenAI model name"""
        return AppConfig.OPENAI_MODEL

    def get_openai_max_tokens(self) -> int:
        """Get OpenAI max tokens setting"""
        return AppConfig.OPENAI_MAX_TOKENS

    def get_openai_temperature(self) -> float:
        """Get OpenAI temperature setting"""
        return AppConfig.OPENAI_TEMPERATURE
