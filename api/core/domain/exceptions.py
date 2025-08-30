"""
Custom exceptions for the email classification system.
These exceptions provide specific error handling for domain operations.
"""


class EmailClassificationError(Exception):
    """Base exception for email classification errors"""
    pass


class InvalidEmailContentError(EmailClassificationError):
    """Raised when email content is invalid or cannot be processed"""
    pass


class EmailTooShortError(InvalidEmailContentError):
    """Raised when email content is too short to process"""
    pass


class EmailTooLongError(InvalidEmailContentError):
    """Raised when email content exceeds maximum length"""
    pass


class ModelNotAvailableError(EmailClassificationError):
    """Raised when required ML model is not available"""
    pass


class ClassificationFailedError(EmailClassificationError):
    """Raised when email classification fails"""
    pass


class ResponseGenerationError(EmailClassificationError):
    """Raised when response generation fails"""
    pass


class ConfigurationError(EmailClassificationError):
    """Raised when system configuration is invalid"""
    pass


class FileProcessingError(EmailClassificationError):
    """Raised when file processing fails"""
    pass


class UnsupportedFileFormatError(FileProcessingError):
    """Raised when file format is not supported"""
    pass
