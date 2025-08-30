"""
Main email processing service implementation.
Orchestrates the complete email processing pipeline following the Single Responsibility Principle.
"""
import logging
from datetime import datetime
from core.interfaces.services import (
    IEmailProcessingService, ITextPreprocessingService,
    IFeatureExtractionService, IClassificationService, IResponseGenerationService
)
from core.domain.models import EmailAnalysis
from core.domain.exceptions import EmailClassificationError

logger = logging.getLogger(__name__)


class EmailProcessingService(IEmailProcessingService):
    """
    Main service that orchestrates the complete email processing pipeline.
    Follows Single Responsibility Principle by focusing on orchestration.
    """

    def __init__(
        self,
        preprocessing_service: ITextPreprocessingService,
        feature_extraction_service: IFeatureExtractionService,
        classification_service: IClassificationService,
        response_service: IResponseGenerationService
    ):
        """
        Initialize the email processing service with all required dependencies.

        Args:
            preprocessing_service: Service for text preprocessing
            feature_extraction_service: Service for feature extraction
            classification_service: Service for email classification
            response_service: Service for response generation
        """
        self._preprocessing_service = preprocessing_service
        self._feature_extraction_service = feature_extraction_service
        self._classification_service = classification_service
        self._response_service = response_service

    def process_email(self, email_content: str) -> EmailAnalysis:
        """
        Process email through the complete pipeline.

        Args:
            email_content: Raw email content

        Returns:
            Complete EmailAnalysis result

        Raises:
            EmailClassificationError: If processing fails at any stage
        """
        start_time = datetime.now()

        try:
            logger.info("Starting email processing pipeline")

            # Step 1: Preprocess the email text
            logger.debug("Step 1: Preprocessing email text")
            processed_email = self._preprocessing_service.preprocess_text(
                email_content)

            # Step 2: Extract features from processed email
            logger.debug("Step 2: Extracting features")
            features = self._feature_extraction_service.extract_features(
                processed_email)

            # Step 3: Classify the email
            logger.debug("Step 3: Classifying email")
            classification = self._classification_service.classify_email(
                processed_email, features)

            # Step 4: Generate response
            logger.debug("Step 4: Generating response")
            response = self._response_service.generate_response(
                email_content, classification, features
            )

            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()

            # Create final analysis result
            analysis = EmailAnalysis(
                category=classification.category,
                confidence=classification.confidence,
                response=response,
                word_count=processed_email.word_count,
                processing_time=round(processing_time, 2),
                keywords_found=features.productive_keywords + features.unproductive_keywords,
                sentiment_score=classification.confidence / 100.0,  # Normalize to 0-1
                timestamp=datetime.now()
            )

            logger.info(
                f"Email processing completed successfully. "
                f"Category: {classification.category.value}, "
                f"Confidence: {classification.confidence}%, "
                f"Processing time: {processing_time:.2f}s"
            )

            return analysis

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(
                f"Email processing failed after {processing_time:.2f}s: {e}")
            raise EmailClassificationError(
                f"Email processing failed: {str(e)}")

    def get_processing_status(self) -> dict:
        """
        Get status of all processing services.

        Returns:
            Dictionary with service status information
        """
        return {
            'preprocessing_available': True,  # Always available
            'feature_extraction_available': True,  # Always available
            'classification_available': self._classification_service.is_classification_available(),
            'response_generation_available': True,  # Always available
            'pipeline_ready': self._classification_service.is_classification_available()
        }
