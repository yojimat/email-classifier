"""
Model repository implementation.
Manages ML model loading and caching following the Repository pattern.
"""
import os
import logging
from typing import Dict, Any, Optional
from transformers import pipeline
from core.interfaces.repositories import IModelRepository
from core.domain.exceptions import ModelNotAvailableError
from core.config import AppConfig

logger = logging.getLogger(__name__)


class ModelRepository(IModelRepository):
    """
    Concrete implementation of model repository.
    Handles ML model lifecycle management.
    """

    def __init__(self):
        """Initialize the model repository"""
        self._models: Dict[str, Any] = {}
        self._model_info: Dict[str, Dict[str, Any]] = {}

        # Ensure model cache directory exists
        os.makedirs(AppConfig.MODEL_CACHE_DIR, exist_ok=True)

    def load_classification_model(self, model_name: str) -> Any:
        """
        Load and return classification model.

        Args:
            model_name: Name of the model to load

        Returns:
            Loaded model pipeline

        Raises:
            ModelNotAvailableError: If model cannot be loaded
        """
        if model_name in self._models:
            logger.info(f"Using cached model: {model_name}")
            return self._models[model_name]

        try:
            logger.info(f"Loading model: {model_name}")

            model = pipeline(
                "sentiment-analysis",
                model=model_name,
                device=AppConfig.get_model_device(),
                cache_dir=AppConfig.MODEL_CACHE_DIR
            )

            # Cache the model
            self._models[model_name] = model
            self._model_info[model_name] = {
                'name': model_name,
                'type': 'sentiment-analysis',
                'device': AppConfig.get_model_device(),
                'loaded': True
            }

            logger.info(f"Model loaded successfully: {model_name}")
            return model

        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise ModelNotAvailableError(
                f"Cannot load model {model_name}: {str(e)}")

    def is_model_available(self, model_name: str) -> bool:
        """
        Check if model is available.

        Args:
            model_name: Name of the model to check

        Returns:
            True if model is available, False otherwise
        """
        if model_name in self._models:
            return True

        try:
            # Try to load the model to check availability
            self.load_classification_model(model_name)
            return True
        except ModelNotAvailableError:
            return False

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a model.

        Args:
            model_name: Name of the model

        Returns:
            Dictionary with model information
        """
        if model_name in self._model_info:
            return self._model_info[model_name].copy()

        return {
            'name': model_name,
            'loaded': False,
            'available': self.is_model_available(model_name)
        }

    def unload_model(self, model_name: str) -> None:
        """
        Unload a model from memory.

        Args:
            model_name: Name of the model to unload
        """
        if model_name in self._models:
            del self._models[model_name]
            if model_name in self._model_info:
                self._model_info[model_name]['loaded'] = False
            logger.info(f"Model unloaded: {model_name}")

    def get_loaded_models(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all loaded models"""
        return {name: info.copy() for name, info in self._model_info.items() if info.get('loaded', False)}
