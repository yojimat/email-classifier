"""
Configuration management for the email classification system.
Centralizes all configuration settings and environment variables.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AppConfig:
    """
    Centralized configuration class following the Single Responsibility Principle.
    Contains all application settings and environment variables.
    """

    # API Configuration
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '5000'))

    # External Service Keys
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    HUGGINGFACE_TOKEN: str = os.getenv('HUGGINGFACE_TOKEN', '')

    # Email Processing Limits
    MAX_EMAIL_LENGTH: int = int(os.getenv('MAX_EMAIL_LENGTH', '10000'))
    MIN_EMAIL_LENGTH: int = int(os.getenv('MIN_EMAIL_LENGTH', '10'))

    # Model Configuration
    USE_GPU: bool = os.getenv('USE_GPU', 'False').lower() == 'true'
    MODEL_CACHE_DIR: str = os.getenv('MODEL_CACHE_DIR', './models')
    CLASSIFICATION_MODEL: str = os.getenv(
        'CLASSIFICATION_MODEL',
        'distilbert-base-uncased-finetuned-sst-2-english'
    )

    # Classification Keywords
    PRODUCTIVE_KEYWORDS: List[str] = [
        'projeto', 'reunião', 'prazo', 'entrega', 'análise', 'relatório',
        'proposta', 'cliente', 'desenvolvimento', 'implementação', 'solução',
        'estratégia', 'planejamento', 'resultado', 'objetivo', 'meta',
        'project', 'meeting', 'deadline', 'delivery', 'analysis', 'report',
        'proposal', 'client', 'development', 'implementation', 'solution',
        'strategy', 'planning', 'result', 'objective', 'goal'
    ]

    UNPRODUCTIVE_KEYWORDS: List[str] = [
        'spam', 'promoção', 'desconto', 'oferta', 'grátis', 'urgente',
        'clique', 'compre', 'newsletter', 'propaganda', 'publicidade',
        'promotion', 'discount', 'offer', 'free', 'urgent', 'click',
        'buy', 'advertisement', 'marketing', 'sale'
    ]

    # File Processing
    SUPPORTED_FILE_FORMATS: List[str] = ['.txt', '.pdf']
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB

    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # OpenAI Configuration
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_MAX_TOKENS: int = int(os.getenv('OPENAI_MAX_TOKENS', '200'))
    OPENAI_TEMPERATURE: float = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

    # Response Templates
    MAX_RESPONSE_LENGTH: int = int(os.getenv('MAX_RESPONSE_LENGTH', '500'))

    @classmethod
    def validate_config(cls) -> None:
        """
        Validate configuration settings.

        Raises:
            ValueError: If configuration is invalid
        """
        if cls.MAX_EMAIL_LENGTH <= cls.MIN_EMAIL_LENGTH:
            raise ValueError(
                "MAX_EMAIL_LENGTH must be greater than MIN_EMAIL_LENGTH")

        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError("PORT must be between 1 and 65535")

        if cls.MAX_FILE_SIZE <= 0:
            raise ValueError("MAX_FILE_SIZE must be positive")

        if not cls.MODEL_CACHE_DIR:
            raise ValueError("MODEL_CACHE_DIR cannot be empty")

    @classmethod
    def get_model_device(cls) -> int:
        """Get device for model loading (-1 for CPU, 0+ for GPU)"""
        return 0 if cls.USE_GPU else -1

    @classmethod
    def is_openai_configured(cls) -> bool:
        """Check if OpenAI is properly configured"""
        return bool(cls.OPENAI_API_KEY)

    @classmethod
    def is_huggingface_configured(cls) -> bool:
        """Check if HuggingFace is properly configured"""
        return bool(cls.HUGGINGFACE_TOKEN)
