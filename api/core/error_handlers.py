"""
Centralized error handling for the email classification system.
Provides consistent error responses and logging across all layers.
"""
import logging
from typing import Tuple, Dict, Any
from flask import jsonify, request
from werkzeug.exceptions import HTTPException

from .domain.exceptions import (
    EmailClassificationError, InvalidEmailContentError, EmailTooShortError,
    EmailTooLongError, ModelNotAvailableError, ClassificationFailedError,
    ResponseGenerationError, ConfigurationError, FileProcessingError,
    UnsupportedFileFormatError
)

logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Centralized error handler that provides consistent error responses
    and logging across the application.
    """

    @staticmethod
    def handle_email_classification_error(error: EmailClassificationError) -> Tuple[Dict[str, Any], int]:
        """Handle email classification errors"""
        logger.error(f"Email classification error: {error}")
        return {
            'error': str(error),
            'error_type': 'EmailClassificationError',
            'request_id': ErrorHandler._get_request_id()
        }, 422

    @staticmethod
    def handle_invalid_email_content_error(error: InvalidEmailContentError) -> Tuple[Dict[str, Any], int]:
        """Handle invalid email content errors"""
        logger.warning(f"Invalid email content: {error}")
        return {
            'error': str(error),
            'error_type': 'InvalidEmailContentError',
            'request_id': ErrorHandler._get_request_id()
        }, 400

    @staticmethod
    def handle_email_too_short_error(error: EmailTooShortError) -> Tuple[Dict[str, Any], int]:
        """Handle email too short errors"""
        logger.warning(f"Email too short: {error}")
        return {
            'error': str(error),
            'error_type': 'EmailTooShortError',
            'request_id': ErrorHandler._get_request_id()
        }, 400

    @staticmethod
    def handle_email_too_long_error(error: EmailTooLongError) -> Tuple[Dict[str, Any], int]:
        """Handle email too long errors"""
        logger.warning(f"Email too long: {error}")
        return {
            'error': str(error),
            'error_type': 'EmailTooLongError',
            'request_id': ErrorHandler._get_request_id()
        }, 400

    @staticmethod
    def handle_model_not_available_error(error: ModelNotAvailableError) -> Tuple[Dict[str, Any], int]:
        """Handle model not available errors"""
        logger.error(f"Model not available: {error}")
        return {
            'error': 'Classification service temporarily unavailable',
            'error_type': 'ModelNotAvailableError',
            'request_id': ErrorHandler._get_request_id()
        }, 503

    @staticmethod
    def handle_classification_failed_error(error: ClassificationFailedError) -> Tuple[Dict[str, Any], int]:
        """Handle classification failed errors"""
        logger.error(f"Classification failed: {error}")
        return {
            'error': 'Email classification failed',
            'error_type': 'ClassificationFailedError',
            'request_id': ErrorHandler._get_request_id()
        }, 422

    @staticmethod
    def handle_response_generation_error(error: ResponseGenerationError) -> Tuple[Dict[str, Any], int]:
        """Handle response generation errors"""
        logger.error(f"Response generation failed: {error}")
        return {
            'error': 'Response generation failed',
            'error_type': 'ResponseGenerationError',
            'request_id': ErrorHandler._get_request_id()
        }, 422

    @staticmethod
    def handle_file_processing_error(error: FileProcessingError) -> Tuple[Dict[str, Any], int]:
        """Handle file processing errors"""
        logger.error(f"File processing error: {error}")
        return {
            'error': str(error),
            'error_type': 'FileProcessingError',
            'request_id': ErrorHandler._get_request_id()
        }, 422

    @staticmethod
    def handle_unsupported_file_format_error(error: UnsupportedFileFormatError) -> Tuple[Dict[str, Any], int]:
        """Handle unsupported file format errors"""
        logger.warning(f"Unsupported file format: {error}")
        return {
            'error': str(error),
            'error_type': 'UnsupportedFileFormatError',
            'request_id': ErrorHandler._get_request_id()
        }, 400

    @staticmethod
    def handle_configuration_error(error: ConfigurationError) -> Tuple[Dict[str, Any], int]:
        """Handle configuration errors"""
        logger.error(f"Configuration error: {error}")
        return {
            'error': 'System configuration error',
            'error_type': 'ConfigurationError',
            'request_id': ErrorHandler._get_request_id()
        }, 500

    @staticmethod
    def handle_http_exception(error: HTTPException) -> Tuple[Dict[str, Any], int]:
        """Handle HTTP exceptions"""
        logger.warning(f"HTTP exception: {error}")
        return {
            'error': error.description,
            'error_type': 'HTTPException',
            'request_id': ErrorHandler._get_request_id()
        }, error.code or 500

    @staticmethod
    def handle_unexpected_error(error: Exception) -> Tuple[Dict[str, Any], int]:
        """Handle unexpected errors"""
        logger.error(f"Unexpected error: {error}", exc_info=True)
        return {
            'error': 'Internal server error',
            'error_type': 'UnexpectedError',
            'request_id': ErrorHandler._get_request_id()
        }, 500

    @staticmethod
    def handle_validation_error(field: str, message: str) -> Tuple[Dict[str, Any], int]:
        """Handle validation errors"""
        logger.warning(f"Validation error for field '{field}': {message}")
        return {
            'error': f"Validation error: {message}",
            'field': field,
            'error_type': 'ValidationError',
            'request_id': ErrorHandler._get_request_id()
        }, 400

    @staticmethod
    def _get_request_id() -> str:
        """Get request ID for tracking"""
        # In a production environment, you might want to use a proper request ID
        # For now, we'll use a simple approach
        try:
            return getattr(request, 'id', 'unknown')
        except:
            return 'unknown'


def register_error_handlers(app):
    """
    Register all error handlers with the Flask application.

    Args:
        app: Flask application instance
    """

    # Domain-specific error handlers
    @app.errorhandler(EmailClassificationError)
    def handle_email_classification_error(error):
        response_data, status_code = ErrorHandler.handle_email_classification_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(InvalidEmailContentError)
    def handle_invalid_email_content_error(error):
        response_data, status_code = ErrorHandler.handle_invalid_email_content_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(EmailTooShortError)
    def handle_email_too_short_error(error):
        response_data, status_code = ErrorHandler.handle_email_too_short_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(EmailTooLongError)
    def handle_email_too_long_error(error):
        response_data, status_code = ErrorHandler.handle_email_too_long_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(ModelNotAvailableError)
    def handle_model_not_available_error(error):
        response_data, status_code = ErrorHandler.handle_model_not_available_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(ClassificationFailedError)
    def handle_classification_failed_error(error):
        response_data, status_code = ErrorHandler.handle_classification_failed_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(ResponseGenerationError)
    def handle_response_generation_error(error):
        response_data, status_code = ErrorHandler.handle_response_generation_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(FileProcessingError)
    def handle_file_processing_error(error):
        response_data, status_code = ErrorHandler.handle_file_processing_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(UnsupportedFileFormatError)
    def handle_unsupported_file_format_error(error):
        response_data, status_code = ErrorHandler.handle_unsupported_file_format_error(
            error)
        return jsonify(response_data), status_code

    @app.errorhandler(ConfigurationError)
    def handle_configuration_error(error):
        response_data, status_code = ErrorHandler.handle_configuration_error(
            error)
        return jsonify(response_data), status_code

    # HTTP exception handler
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response_data, status_code = ErrorHandler.handle_http_exception(error)
        return jsonify(response_data), status_code

    # Catch-all exception handler
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        response_data, status_code = ErrorHandler.handle_unexpected_error(
            error)
        return jsonify(response_data), status_code
