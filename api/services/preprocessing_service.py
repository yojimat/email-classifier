"""
Text preprocessing service implementation.
Handles all text preprocessing operations following the Single Responsibility Principle.
"""
import re
import logging
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

from core.interfaces.services import ITextPreprocessingService
from core.interfaces.repositories import IConfigRepository
from core.domain.models import ProcessedEmail
from core.domain.exceptions import InvalidEmailContentError, EmailTooShortError, EmailTooLongError

logger = logging.getLogger(__name__)


class TextPreprocessingService(ITextPreprocessingService):
    """
    Service responsible for text preprocessing operations.
    Follows Single Responsibility Principle by focusing only on text processing.
    """

    def __init__(self, config_repository: IConfigRepository):
        """
        Initialize the preprocessing service.

        Args:
            config_repository: Repository for accessing configuration
        """
        self._config_repo = config_repository
        self._stemmer = PorterStemmer()
        self._lemmatizer = WordNetLemmatizer()

        # Initialize NLTK resources
        self._initialize_nltk()

        # Load stop words
        self._stop_words = set(
            stopwords.words('portuguese') +
            stopwords.words('english')
        )

    def _initialize_nltk(self) -> None:
        """Initialize required NLTK resources"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            logger.info("NLTK resources initialized successfully")
        except Exception as e:
            logger.warning(f"Error downloading NLTK resources: {e}")

    def validate_email_content(self, text: str) -> None:
        """
        Validate email content meets requirements.

        Args:
            text: Email text to validate

        Raises:
            InvalidEmailContentError: If content is invalid
            EmailTooShortError: If content is too short
            EmailTooLongError: If content is too long
        """
        if not text or not text.strip():
            raise InvalidEmailContentError("Email content cannot be empty")

        text_length = len(text.strip())
        min_length = self._config_repo.get_min_email_length()
        max_length = self._config_repo.get_max_email_length()

        if text_length < min_length:
            raise EmailTooShortError(
                f"Email content too short. Minimum length: {min_length}, "
                f"provided: {text_length}"
            )

        if text_length > max_length:
            raise EmailTooLongError(
                f"Email content too long. Maximum length: {max_length}, "
                f"provided: {text_length}"
            )

    def preprocess_text(self, text: str) -> ProcessedEmail:
        """
        Preprocess email text including tokenization, cleaning, and normalization.

        Args:
            text: Raw email text

        Returns:
            ProcessedEmail object with all preprocessing results
        """
        # Validate input
        self.validate_email_content(text)

        # Clean and normalize text
        cleaned_text = self._clean_text(text)

        # Tokenization
        tokens = self._tokenize_text(cleaned_text)

        # Filter tokens (remove stop words and short words)
        filtered_tokens = self._filter_tokens(tokens)

        # Lemmatization
        lemmatized_tokens = self._lemmatize_tokens(filtered_tokens)

        # Stemming
        stemmed_tokens = self._stem_tokens(lemmatized_tokens)

        # Create processed text
        processed_text = ' '.join(lemmatized_tokens)

        return ProcessedEmail(
            original_text=text,
            tokens=tokens,
            filtered_tokens=filtered_tokens,
            lemmatized_tokens=lemmatized_tokens,
            stemmed_tokens=stemmed_tokens,
            processed_text=processed_text,
            word_count=len(tokens)
        )

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text.

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters but keep accented characters
        text = re.sub(r'[^\w\s\u00C0-\u00FF]', ' ', text)

        # Remove extra spaces
        text = text.strip()

        return text

    def _tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text into words.

        Args:
            text: Cleaned text

        Returns:
            List of tokens
        """
        try:
            tokens = word_tokenize(text.lower())
            return tokens
        except Exception as e:
            logger.warning(f"Error in tokenization, using simple split: {e}")
            # Fallback to simple split
            return text.lower().split()

    def _filter_tokens(self, tokens: List[str]) -> List[str]:
        """
        Filter tokens by removing stop words and short words.

        Args:
            tokens: List of tokens

        Returns:
            Filtered tokens
        """
        filtered = [
            token for token in tokens
            if token not in self._stop_words and len(token) > 2
        ]
        return filtered

    def _lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens to their base form.

        Args:
            tokens: List of tokens

        Returns:
            Lemmatized tokens
        """
        try:
            lemmatized = [self._lemmatizer.lemmatize(
                token) for token in tokens]
            return lemmatized
        except Exception as e:
            logger.warning(f"Error in lemmatization: {e}")
            return tokens  # Return original tokens if lemmatization fails

    def _stem_tokens(self, tokens: List[str]) -> List[str]:
        """
        Stem tokens to their root form.

        Args:
            tokens: List of tokens

        Returns:
            Stemmed tokens
        """
        try:
            stemmed = [self._stemmer.stem(token) for token in tokens]
            return stemmed
        except Exception as e:
            logger.warning(f"Error in stemming: {e}")
            return tokens  # Return original tokens if stemming fails
