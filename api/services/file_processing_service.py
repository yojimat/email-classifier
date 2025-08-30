"""
File processing service implementation.
Handles file processing operations following the Single Responsibility Principle.
"""
import logging
from core.interfaces.services import IFileProcessingService, IEmailProcessingService
from core.interfaces.repositories import IFileRepository
from core.domain.models import EmailAnalysis
from core.domain.exceptions import FileProcessingError

logger = logging.getLogger(__name__)


class FileProcessingService(IFileProcessingService):
    """
    Service responsible for processing files and extracting email content.
    Follows Single Responsibility Principle by focusing only on file operations.
    """

    def __init__(
        self,
        file_repository: IFileRepository,
        email_processing_service: IEmailProcessingService
    ):
        """
        Initialize the file processing service.

        Args:
            file_repository: Repository for file operations
            email_processing_service: Service for processing extracted email content
        """
        self._file_repo = file_repository
        self._email_service = email_processing_service

    def process_file(self, file_data: bytes, filename: str) -> EmailAnalysis:
        """
        Process file and extract email content for analysis.

        Args:
            file_data: File content as bytes
            filename: Name of the file

        Returns:
            EmailAnalysis result

        Raises:
            FileProcessingError: If file processing fails
        """
        try:
            logger.info(f"Processing file: {filename}")

            # Extract text from file
            extracted_text = self.extract_text_from_file(file_data, filename)

            # Process the extracted text as email content
            analysis = self._email_service.process_email(extracted_text)

            logger.info(f"File processing completed successfully: {filename}")
            return analysis

        except Exception as e:
            logger.error(f"File processing failed for {filename}: {e}")
            raise FileProcessingError(
                f"Failed to process file {filename}: {str(e)}")

    def extract_text_from_file(self, file_data: bytes, filename: str) -> str:
        """
        Extract text content from file.

        Args:
            file_data: File content as bytes
            filename: Name of the file

        Returns:
            Extracted text content

        Raises:
            FileProcessingError: If text extraction fails
        """
        try:
            logger.debug(f"Extracting text from file: {filename}")

            # Use repository to extract text based on file type
            extracted_text = self._file_repo.extract_text_from_file(
                file_data, filename)

            if not extracted_text or not extracted_text.strip():
                raise FileProcessingError(
                    f"No text content found in file: {filename}")

            logger.debug(
                f"Successfully extracted {len(extracted_text)} characters from {filename}")
            return extracted_text

        except Exception as e:
            logger.error(f"Text extraction failed for {filename}: {e}")
            raise FileProcessingError(
                f"Failed to extract text from {filename}: {str(e)}")

    def is_file_supported(self, filename: str) -> bool:
        """
        Check if file format is supported.

        Args:
            filename: Name of the file

        Returns:
            True if file format is supported
        """
        return self._file_repo.is_supported_format(filename)

    def get_supported_formats(self) -> list:
        """
        Get list of supported file formats.

        Returns:
            List of supported file extensions
        """
        return self._file_repo.get_supported_formats()
