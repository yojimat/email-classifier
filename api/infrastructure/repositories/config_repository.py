"""
Configuration repository implementation.
Provides access to application configuration following the Repository pattern.
"""
from typing import List
from core.interfaces.repositories import IConfigRepository
from core.config import AppConfig


class ConfigRepository(IConfigRepository):
    """
    Concrete implementation of configuration repository.
    Encapsulates access to application configuration.
    """

    def __init__(self):
        """Initialize the configuration repository"""
        # Validate configuration on initialization
        AppConfig.validate_config()

    def get_max_email_length(self) -> int:
        """Get maximum allowed email length"""
        return AppConfig.MAX_EMAIL_LENGTH

    def get_min_email_length(self) -> int:
        """Get minimum required email length"""
        return AppConfig.MIN_EMAIL_LENGTH

    def get_productive_keywords(self) -> List[str]:
        """Get list of productive keywords"""
        return AppConfig.PRODUCTIVE_KEYWORDS.copy()

    def get_unproductive_keywords(self) -> List[str]:
        """Get list of unproductive keywords"""
        return AppConfig.UNPRODUCTIVE_KEYWORDS.copy()

    def get_classification_model_name(self) -> str:
        """Get the name of the classification model"""
        return AppConfig.CLASSIFICATION_MODEL

    def get_model_cache_dir(self) -> str:
        """Get model cache directory path"""
        return AppConfig.MODEL_CACHE_DIR

    def is_gpu_enabled(self) -> bool:
        """Check if GPU usage is enabled"""
        return AppConfig.USE_GPU
