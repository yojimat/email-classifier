"""
Model repository implementation.
Manages ML model loading and caching 
"""
import os
import logging
from typing import Dict, Any
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
                task="sentiment-analysis",
                model=model_name,
                device=AppConfig.get_model_device()
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
