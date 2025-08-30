"""
Feature extraction service implementation.
Handles feature extraction from processed emails following the Single Responsibility Principle.
"""
import re
import logging
from typing import List
from core.interfaces.services import IFeatureExtractionService
from core.interfaces.repositories import IConfigRepository
from core.domain.models import ProcessedEmail, EmailFeatures

logger = logging.getLogger(__name__)


class FeatureExtractionService(IFeatureExtractionService):
    """
    Service responsible for extracting features from processed emails.
    Follows Single Responsibility Principle by focusing only on feature extraction.
    """

    def __init__(self, config_repository: IConfigRepository):
        """
        Initialize the feature extraction service.

        Args:
            config_repository: Repository for accessing configuration
        """
        self._config_repo = config_repository

    def extract_features(self, processed_email: ProcessedEmail) -> EmailFeatures:
        """
        Extract features from processed email for classification.

        Args:
            processed_email: Preprocessed email data

        Returns:
            EmailFeatures object with extracted features
        """
        # Get configuration data
        productive_keywords = self._config_repo.get_productive_keywords()
        unproductive_keywords = self._config_repo.get_unproductive_keywords()

        # Extract keyword-based features
        productive_matches = self._find_keyword_matches(
            processed_email.processed_text,
            productive_keywords
        )

        unproductive_matches = self._find_keyword_matches(
            processed_email.processed_text,
            unproductive_keywords
        )

        # Extract text-based features
        text_features = self._extract_text_features(processed_email)

        # Extract pattern-based features
        pattern_features = self._extract_pattern_features(
            processed_email.original_text)

        return EmailFeatures(
            text_length=len(processed_email.processed_text),
            word_count=processed_email.word_count,
            avg_word_length=self._calculate_avg_word_length(
                processed_email.filtered_tokens),
            productive_keywords=productive_matches,
            unproductive_keywords=unproductive_matches,
            productive_score=len(productive_matches),
            unproductive_score=len(unproductive_matches),
            has_urls=pattern_features['has_urls'],
            has_numbers=pattern_features['has_numbers'],
            exclamation_count=pattern_features['exclamation_count'],
            question_count=pattern_features['question_count']
        )

    def _find_keyword_matches(self, text: str, keywords: List[str]) -> List[str]:
        """
        Find keyword matches in text.

        Args:
            text: Text to search in
            keywords: List of keywords to search for

        Returns:
            List of matched keywords
        """
        text_lower = text.lower()
        matches = []

        for keyword in keywords:
            if keyword.lower() in text_lower:
                matches.append(keyword)

        return matches

    def _extract_text_features(self, processed_email: ProcessedEmail) -> dict:
        """
        Extract text-based features.

        Args:
            processed_email: Processed email data

        Returns:
            Dictionary of text features
        """
        return {
            'token_count': len(processed_email.tokens),
            'filtered_token_count': len(processed_email.filtered_tokens),
            'unique_tokens': len(set(processed_email.filtered_tokens)),
            'text_complexity': self._calculate_text_complexity(processed_email)
        }

    def _extract_pattern_features(self, original_text: str) -> dict:
        """
        Extract pattern-based features from original text.

        Args:
            original_text: Original email text

        Returns:
            Dictionary of pattern features
        """
        return {
            'has_urls': bool(re.findall(r'http[s]?://\S+', original_text)),
            'has_numbers': bool(re.findall(r'\d+', original_text)),
            'exclamation_count': original_text.count('!'),
            'question_count': original_text.count('?'),
            'uppercase_ratio': self._calculate_uppercase_ratio(original_text),
            'has_email_addresses': bool(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', original_text))
        }

    def _calculate_avg_word_length(self, tokens: List[str]) -> float:
        """
        Calculate average word length.

        Args:
            tokens: List of tokens

        Returns:
            Average word length
        """
        if not tokens:
            return 0.0

        total_length = sum(len(token) for token in tokens)
        return total_length / len(tokens)

    def _calculate_text_complexity(self, processed_email: ProcessedEmail) -> float:
        """
        Calculate text complexity score.

        Args:
            processed_email: Processed email data

        Returns:
            Complexity score
        """
        if not processed_email.filtered_tokens:
            return 0.0

        # Simple complexity measure based on vocabulary diversity
        unique_tokens = len(set(processed_email.filtered_tokens))
        total_tokens = len(processed_email.filtered_tokens)

        return unique_tokens / total_tokens if total_tokens > 0 else 0.0

    def _calculate_uppercase_ratio(self, text: str) -> float:
        """
        Calculate ratio of uppercase characters.

        Args:
            text: Text to analyze

        Returns:
            Ratio of uppercase characters
        """
        if not text:
            return 0.0

        letters = [c for c in text if c.isalpha()]
        if not letters:
            return 0.0

        uppercase_count = sum(1 for c in letters if c.isupper())
        return uppercase_count / len(letters)
