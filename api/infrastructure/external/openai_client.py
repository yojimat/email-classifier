"""
OpenAI client implementation.
Handles direct integration with OpenAI API following the Repository pattern.
"""
import logging
from typing import Optional
import openai
from ...core.interfaces.repositories import IExternalServiceRepository

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Client for OpenAI API integration.
    Encapsulates all OpenAI-specific operations.
    """
    
    def __init__(self, external_service_repo: IExternalServiceRepository):
        """
        Initialize OpenAI client.
        
        Args:
            external_service_repo: Repository for external service configurations
        """
        self._external_repo = external_service_repo
        self._is_configured = False
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize OpenAI client"""
        try:
            api_key = self._external_repo.get_openai_api_key()
            if api_key:
                openai.api_key = api_key
                self._is_configured = True
                logger.info("OpenAI client initialized successfully")
            else:
                logger.info("OpenAI API key not configured")
                self._is_configured = False
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI client: {e}")
            self._is_configured = False
    
    def is_available(self) -> bool:
        """Check if OpenAI client is available"""
        return self._is_configured
    
    def generate_chat_completion(self, messages: list, **kwargs) -> Optional[str]:
        """
        Generate chat completion using OpenAI.
        
        Args:
            messages: List of messages for the conversation
            **kwargs: Additional parameters for the API call
            
        Returns:
            Generated response or None if failed
        """
        if not self.is_available():
            return None
        
        try:
            response = openai.ChatCompletion.create(
                model=self._external_repo.get_openai_model_name(),
                messages=messages,
                max_tokens=self._external_repo.get_openai_max_tokens(),
                temperature=self._external_repo.get_openai_temperature(),
                **kwargs
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to OpenAI API.
        
        Returns:
            True if connection is successful
        """
        if not self.is_available():
            return False
        
        try:
            response = self.generate_chat_completion(
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            return response is not None
            
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False
