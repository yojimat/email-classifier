"""
Domain models for the email classification system.
These models represent the core business entities and value objects.
"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from datetime import datetime


class EmailCategory(Enum):
    """Email classification categories"""
    PRODUCTIVE = "productive"
    UNPRODUCTIVE = "unproductive"


@dataclass(frozen=True)
class EmailAnalysis:
    """
    Immutable value object representing the result of email analysis.
    Contains all information about the classification and processing.
    """
    category: EmailCategory
    confidence: float
    response: str
    word_count: int
    processing_time: float
    keywords_found: List[str]
    sentiment_score: float = 0.0
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Validate the analysis data"""
        if not 0 <= self.confidence <= 100:
            raise ValueError("Confidence must be between 0 and 100")
        if self.word_count < 0:
            raise ValueError("Word count cannot be negative")
        if self.processing_time < 0:
            raise ValueError("Processing time cannot be negative")


@dataclass(frozen=True)
class ProcessedEmail:
    """
    Value object representing preprocessed email data.
    Contains the original text and all processed variations.
    """
    original_text: str
    tokens: List[str]
    filtered_tokens: List[str]
    lemmatized_tokens: List[str]
    stemmed_tokens: List[str]
    processed_text: str
    word_count: int


@dataclass(frozen=True)
class EmailFeatures:
    """
    Value object containing extracted features from an email.
    Used for classification and analysis.
    """
    text_length: int
    word_count: int
    avg_word_length: float
    productive_keywords: List[str]
    unproductive_keywords: List[str]
    productive_score: int
    unproductive_score: int
    has_urls: bool
    has_numbers: bool
    exclamation_count: int
    question_count: int


@dataclass(frozen=True)
class ClassificationResult:
    """
    Value object representing the result of email classification.
    Separate from EmailAnalysis to maintain single responsibility.
    """
    category: EmailCategory
    confidence: float
    method_used: str
    features_used: List[str]


@dataclass(frozen=True)
class ResponseTemplate:
    """
    Value object representing a response template.
    """
    template_id: str
    category: EmailCategory
    template_text: str
    context_variables: List[str]
