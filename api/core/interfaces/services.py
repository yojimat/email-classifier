"""
Service interfaces following the Dependency Inversion Principle.
These abstractions define contracts for business logic operations.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from ..domain.models import (
    EmailAnalysis, ProcessedEmail, EmailFeatures,
    ClassificationResult, EmailCategory
)


class ITextPreprocessingService(ABC):
    """Interface for text preprocessing operations"""

    @abstractmethod
    def preprocess_text(self, text: str) -> ProcessedEmail:
        """
        Preprocess email text including tokenization, cleaning, and normalization.

        Args:
            text: Raw email text

        Returns:
            ProcessedEmail object with all preprocessing results
        """
        pass

    @abstractmethod
    def validate_email_content(self, text: str) -> None:
        """
        Validate email content meets requirements.

        Args:
            text: Email text to validate

        Raises:
            InvalidEmailContentError: If content is invalid
        """
        pass


class IFeatureExtractionService(ABC):
    """Interface for feature extraction from processed emails"""

    @abstractmethod
    def extract_features(self, processed_email: ProcessedEmail) -> EmailFeatures:
        """
        Extract features from processed email for classification.

        Args:
            processed_email: Preprocessed email data

        Returns:
            EmailFeatures object with extracted features
        """
        pass


class IClassificationService(ABC):
    """Interface for email classification operations"""

    @abstractmethod
    def classify_email(self, processed_email: ProcessedEmail, features: EmailFeatures) -> ClassificationResult:
        """
        Classify email as productive or unproductive.

        Args:
            processed_email: Preprocessed email data
            features: Extracted features

        Returns:
            ClassificationResult with category and confidence
        """
        pass


class IResponseGenerationService(ABC):
    """Interface for response generation operations"""

    @abstractmethod
    def generate_response(self, original_text: str, classification: ClassificationResult, features: EmailFeatures) -> str:
        """
        Generate appropriate response based on classification.

        Args:
            original_text: Original email text
            classification: Classification result
            features: Email features

        Returns:
            Generated response text
        """
        pass


class IEmailProcessingService(ABC):
    """Interface for the main email processing orchestration"""

    @abstractmethod
    def process_email(self, email_content: str) -> EmailAnalysis:
        """
        Process email through the complete pipeline.

        Args:
            email_content: Raw email content

        Returns:
            Complete EmailAnalysis result
        """
        pass


class IFileProcessingService(ABC):
    """Interface for file processing operations"""

    @abstractmethod
    def process_file(self, file_data: bytes, filename: str) -> EmailAnalysis:
        """
        Process file and extract email content for analysis.

        Args:
            file_data: File content as bytes
            filename: Name of the file

        Returns:
            EmailAnalysis result
        """
        pass

    @abstractmethod
    def extract_text_from_file(self, file_data: bytes, filename: str) -> str:
        """
        Extract text content from file.

        Args:
            file_data: File content as bytes
            filename: Name of the file

        Returns:
            Extracted text content
        """
        pass

    @abstractmethod
    def is_file_supported(self, filename: str) -> bool:
        """
        Check if file format is supported.

        Args:
            filename: Name of the file

        Returns:
            True if file format is supported
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> list:
        """
        Get list of supported file formats.

        Returns:
            List of supported file extensions
        """
        pass


class IExternalAIService(ABC):
    """Interface for external AI service integrations"""

    @abstractmethod
    def generate_ai_response(self, text: str, category: EmailCategory) -> str:
        """
        Generate response using external AI service.

        Args:
            text: Email text
            category: Classification category

        Returns:
            AI-generated response
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if external AI service is available"""
        pass
