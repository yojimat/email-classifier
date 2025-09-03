"""
Classification service implementation.
Handles email classification operations following the Single Responsibility Principle.
"""
import logging
from typing import Tuple
from core.interfaces.services import IClassificationService
from core.interfaces.repositories import IModelRepository, IConfigRepository
from core.domain.models import ProcessedEmail, EmailFeatures, ClassificationResult, EmailCategory
from core.domain.exceptions import ClassificationFailedError, ModelNotAvailableError

logger = logging.getLogger(__name__)


class ClassificationService(IClassificationService):
    """
    Service responsible for email classification operations.
    Follows Single Responsibility Principle by focusing only on classification logic.
    """

    def __init__(self, model_repository: IModelRepository, config_repository: IConfigRepository):
        """
        Initialize the classification service.

        Args:
            model_repository: Repository for accessing ML models
            config_repository: Repository for accessing configuration
        """
        self._model_repo = model_repository
        self._config_repo = config_repository
        self._classifier = None
        self._initialize_classifier()

    def _initialize_classifier(self) -> None:
        """Initialize the classification model"""
        try:
            model_name = self._config_repo.get_classification_model_name()
            self._classifier = self._model_repo.load_classification_model(
                model_name)
            logger.info("Classification model initialized successfully")
        except ModelNotAvailableError as e:
            logger.warning(f"ML model not available: {e}")
            self._classifier = None

    def classify_email(self, processed_email: ProcessedEmail, features: EmailFeatures) -> ClassificationResult:
        """
        Classify email as productive or unproductive.

        Args:
            processed_email: Preprocessed email data
            features: Extracted features

        Returns:
            ClassificationResult with category and confidence
        """
        try:
            # Try ML-based classification first if available
            if self._classifier and self._is_suitable_for_ml_classification(processed_email):
                return self._ml_classification(processed_email, features)
            else:
                # Fallback to rule-based classification
                return self._rule_based_classification(features)

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            raise ClassificationFailedError(
                f"Failed to classify email: {str(e)}")

    def _is_suitable_for_ml_classification(self, processed_email: ProcessedEmail) -> bool:
        """
        Check if email is suitable for ML classification.

        Args:
            processed_email: Processed email data

        Returns:
            True if suitable for ML classification
        """
        min_length = self._config_repo.get_min_email_length()
        return len(processed_email.processed_text) > min_length

    def _ml_classification(self, processed_email: ProcessedEmail, features: EmailFeatures) -> ClassificationResult:
        """
        Perform ML-based classification.

        Args:
            processed_email: Processed email data
            features: Email features

        Returns:
            Classification result
        """
        try:
            # Limit text length for model input (most models have token limits)
            text_input = processed_email.processed_text[:512]

            if self._classifier is None:
                raise ModelNotAvailableError("Classifier model is not loaded")

            # Get ML prediction
            ml_result = self._classifier(text_input)
            ml_confidence = ml_result[0]['score']
            ml_label = ml_result[0]['label']

            # Combine ML prediction with keyword-based features
            category, confidence = self._combine_ml_and_rules(
                ml_label, ml_confidence, features
            )

            return ClassificationResult(
                category=category,
                confidence=round(confidence * 100, 1),
                method_used="ml_with_rules",
                features_used=["ml_sentiment", "keywords", "text_patterns"]
            )

        except Exception as e:
            logger.warning(
                f"ML classification failed, falling back to rules: {e}")
            return self._rule_based_classification(features)

    def _combine_ml_and_rules(self, ml_label: str, ml_confidence: float, features: EmailFeatures) -> Tuple[EmailCategory, float]:
        """
        Combine ML prediction with rule-based features.

        Args:
            ml_label: ML model label
            ml_confidence: ML model confidence
            features: Email features

        Returns:
            Tuple of (category, confidence)
        """
        keyword_score = features.productive_score - features.unproductive_score

        # Map ML sentiment to productivity
        if ml_label == 'POSITIVE':
            if keyword_score >= 0:
                category = EmailCategory.PRODUCTIVE
                confidence = ml_confidence
            else:
                # Positive sentiment but negative keywords - reduce confidence
                category = EmailCategory.UNPRODUCTIVE
                confidence = ml_confidence * 0.8
        else:  # NEGATIVE
            if keyword_score > 2:
                # Strong positive keywords override negative sentiment
                category = EmailCategory.PRODUCTIVE
                confidence = 0.7
            else:
                category = EmailCategory.UNPRODUCTIVE
                confidence = ml_confidence

        # Adjust confidence based on additional features
        confidence = self._adjust_confidence_with_features(
            confidence, features, category)

        return category, confidence

    def _rule_based_classification(self, features: EmailFeatures) -> ClassificationResult:
        """
        Perform rule-based classification.

        Args:
            features: Email features

        Returns:
            Classification result
        """
        score = 0
        max_score = 0
        features_used = []

        # Keyword scoring (high weight)
        if features.productive_score > 0:
            score += features.productive_score * 3
            max_score += features.productive_score * 3
            features_used.append("productive_keywords")

        if features.unproductive_score > 0:
            score -= features.unproductive_score * 3
            max_score += features.unproductive_score * 3
            features_used.append("unproductive_keywords")

        # Text length scoring
        if 50 < features.word_count < 500:
            score += 2
            max_score += 2
            features_used.append("optimal_length")
        elif features.word_count < 30:
            score -= 1
            max_score += 1
            features_used.append("short_length")

        # URL presence (suspicious for spam)
        if features.has_urls:
            score -= 1
            max_score += 1
            features_used.append("has_urls")

        # Excessive punctuation
        if features.exclamation_count > 3:
            score -= 2
            max_score += 2
            features_used.append("excessive_exclamation")

        # Determine category and confidence
        if score > 0:
            category = EmailCategory.PRODUCTIVE
            confidence = min(0.5 + (score / (max_score + 1)) * 0.4, 0.95)
        else:
            category = EmailCategory.UNPRODUCTIVE
            confidence = min(0.5 + (abs(score) / (max_score + 1)) * 0.4, 0.95)

        return ClassificationResult(
            category=category,
            confidence=round(confidence * 100, 1),
            method_used="rule_based",
            features_used=features_used
        )

    def _adjust_confidence_with_features(self, base_confidence: float, features: EmailFeatures, category: EmailCategory) -> float:
        """
        Adjust confidence based on additional features.

        Args:
            base_confidence: Base confidence score
            features: Email features
            category: Predicted category

        Returns:
            Adjusted confidence
        """
        confidence = base_confidence

        # URLs + excessive exclamation often indicate spam
        if features.has_urls and features.exclamation_count > 2:
            if category == EmailCategory.UNPRODUCTIVE:
                confidence = min(confidence + 0.1, 0.99)
            else:
                confidence = max(confidence - 0.1, 0.3)

        # Very short emails are often unproductive
        if features.word_count < 20:
            if category == EmailCategory.UNPRODUCTIVE:
                confidence = min(confidence + 0.05, 0.99)
            else:
                confidence = max(confidence - 0.05, 0.3)

        return confidence
