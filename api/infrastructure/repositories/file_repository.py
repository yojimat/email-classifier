"""
File repository implementation.
Handles file processing operations following the Repository pattern.
"""
import logging
from typing import List
import PyPDF2
from io import BytesIO
from core.interfaces.repositories import IFileRepository
from core.domain.exceptions import FileProcessingError, UnsupportedFileFormatError
from core.config import AppConfig

logger = logging.getLogger(__name__)


class FileRepository(IFileRepository):
    """
    Concrete implementation of file repository.
    Handles various file format processing operations.
    """

    def extract_text_from_pdf(self, file_data: bytes) -> str:
        """
        Extract text from PDF file.

        Args:
            file_data: PDF file content as bytes

        Returns:
            Extracted text content

        Raises:
            FileProcessingError: If PDF processing fails
        """
        try:
            pdf_file = BytesIO(file_data)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            extracted_text = text.strip()

            if not extracted_text:
                raise FileProcessingError(
                    "No text could be extracted from PDF")

            logger.info(
                f"Successfully extracted {len(extracted_text)} characters from PDF")
            return extracted_text

        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise FileProcessingError(f"Failed to process PDF file: {str(e)}")

    def extract_text_from_txt(self, file_data: bytes) -> str:
        """
        Extract text from text file.

        Args:
            file_data: Text file content as bytes

        Returns:
            Extracted text content

        Raises:
            FileProcessingError: If text processing fails
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']

            for encoding in encodings:
                try:
                    text = file_data.decode(encoding)
                    logger.info(
                        f"Successfully decoded text file using {encoding} encoding")
                    return text.strip()
                except UnicodeDecodeError:
                    continue

            # If all encodings fail, try with error handling
            text = file_data.decode('utf-8', errors='replace')
            logger.warning("Used UTF-8 with error replacement for text file")
            return text.strip()

        except Exception as e:
            logger.error(f"Error processing text file: {e}")
            raise FileProcessingError(f"Failed to process text file: {str(e)}")

    def is_supported_format(self, filename: str) -> bool:
        """
        Check if file format is supported.

        Args:
            filename: Name of the file

        Returns:
            True if format is supported, False otherwise
        """
        if not filename:
            return False

        # Get file extension
        file_extension = self._get_file_extension(filename)
        return file_extension in AppConfig.SUPPORTED_FILE_FORMATS

    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        return AppConfig.SUPPORTED_FILE_FORMATS.copy()

    def validate_file_size(self, file_data: bytes) -> None:
        """
        Validate file size against maximum allowed size.

        Args:
            file_data: File content as bytes

        Raises:
            FileProcessingError: If file is too large
        """
        file_size = len(file_data)
        if file_size > AppConfig.MAX_FILE_SIZE:
            raise FileProcessingError(
                f"File size ({file_size} bytes) exceeds maximum allowed size "
                f"({AppConfig.MAX_FILE_SIZE} bytes)"
            )

    def _get_file_extension(self, filename: str) -> str:
        """
        Get file extension from filename.

        Args:
            filename: Name of the file

        Returns:
            File extension including the dot (e.g., '.pdf')
        """
        if '.' not in filename:
            return ''

        return '.' + filename.rsplit('.', 1)[1].lower()

    def extract_text_from_file(self, file_data: bytes, filename: str) -> str:
        """
        Extract text from file based on its format.

        Args:
            file_data: File content as bytes
            filename: Name of the file

        Returns:
            Extracted text content

        Raises:
            UnsupportedFileFormatError: If file format is not supported
            FileProcessingError: If file processing fails
        """
        # Validate file size
        self.validate_file_size(file_data)

        # Check if format is supported
        if not self.is_supported_format(filename):
            raise UnsupportedFileFormatError(
                f"File format not supported. Supported formats: {self.get_supported_formats()}"
            )

        file_extension = self._get_file_extension(filename)

        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_data)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(file_data)
        else:
            raise UnsupportedFileFormatError(
                f"Unsupported file format: {file_extension}")
