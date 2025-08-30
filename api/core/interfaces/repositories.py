"""
Repository interfaces following the Repository pattern.
These abstractions define contracts for data access operations.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from core.domain.models import ResponseTemplate, EmailCategory


class IConfigRepository(ABC):
    """Interface for configuration data access"""

    @abstractmethod
    def get_max_email_length(self) -> int:
        """Get maximum allowed email length"""
        pass

    @abstractmethod
    def get_min_email_length(self) -> int:
        """Get minimum required email length"""
        pass

    @abstractmethod
    def get_productive_keywords(self) -> List[str]:
        """Get list of productive keywords"""
        pass

    @abstractmethod
    def get_unproductive_keywords(self) -> List[str]:
        """Get list of unproductive keywords"""
        pass

    @abstractmethod
    def get_classification_model_name(self) -> str:
        """Get the name of the classification model"""
        pass

    @abstractmethod
    def get_model_cache_dir(self) -> str:
        """Get model cache directory path"""
        pass

    @abstractmethod
    def is_gpu_enabled(self) -> bool:
        """Check if GPU usage is enabled"""
        pass


class IModelRepository(ABC):
    """Interface for ML model management"""

    @abstractmethod
    def load_classification_model(self, model_name: str) -> Any:
        """Load and return classification model"""
        pass

    @abstractmethod
    def is_model_available(self, model_name: str) -> bool:
        """Check if model is available"""
        pass

    @abstractmethod
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a model"""
        pass


class IFileRepository(ABC):
    """Interface for file processing operations"""

    @abstractmethod
    def extract_text_from_pdf(self, file_data: bytes) -> str:
        """Extract text from PDF file"""
        pass

    @abstractmethod
    def extract_text_from_txt(self, file_data: bytes) -> str:
        """Extract text from text file"""
        pass

    @abstractmethod
    def is_supported_format(self, filename: str) -> bool:
        """Check if file format is supported"""
        pass

    @abstractmethod
    def extract_text_from_file(self, file_data: bytes, filename: str) -> str:
        """Extract text from file based on its format"""
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        pass


class IResponseTemplateRepository(ABC):
    """Interface for response template management"""

    @abstractmethod
    def get_templates_by_category(self, category: EmailCategory) -> List[ResponseTemplate]:
        """Get response templates for a specific category"""
        pass

    @abstractmethod
    def get_template_by_id(self, template_id: str) -> Optional[ResponseTemplate]:
        """Get a specific template by ID"""
        pass


class IExternalServiceRepository(ABC):
    """Interface for external service integrations"""

    @abstractmethod
    def get_openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        pass

    @abstractmethod
    def get_huggingface_token(self) -> Optional[str]:
        """Get HuggingFace token"""
        pass

    @abstractmethod
    def is_openai_configured(self) -> bool:
        """Check if OpenAI is properly configured"""
        pass

    @abstractmethod
    def get_openai_model_name(self) -> str:
        """Get OpenAI model name"""
        pass

    @abstractmethod
    def get_openai_max_tokens(self) -> int:
        """Get OpenAI max tokens setting"""
        pass

    @abstractmethod
    def get_openai_temperature(self) -> float:
        """Get OpenAI temperature setting"""
        pass
