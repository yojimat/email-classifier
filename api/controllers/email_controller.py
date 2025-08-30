"""
Email controller implementation.
Handles HTTP requests for email processing endpoints following the Single Responsibility Principle.
"""
import logging
from flask import request, jsonify
from core.interfaces.services import IEmailProcessingService, IFileProcessingService
from core.domain.exceptions import (
    EmailClassificationError, InvalidEmailContentError,
    FileProcessingError, UnsupportedFileFormatError
)

logger = logging.getLogger(__name__)


class EmailController:
    """
    Controller responsible for handling email-related HTTP requests.
    """

    def __init__(
        self,
        email_processing_service: IEmailProcessingService,
        file_processing_service: IFileProcessingService
    ):
        """
        Initialize the email controller.

        Args:
            email_processing_service: Service for email processing
            file_processing_service: Service for file processing
        """
        self._email_service = email_processing_service
        self._file_service = file_processing_service

    def classify_email(self):
        """
        Handle email classification requests.

        Expected JSON:
        {
            "email_content": "conteúdo do email..."
        }

        Returns:
            JSON response with classification results
        """
        try:
            # Validate request
            if not request.is_json:
                return jsonify({
                    'error': 'Content-Type deve ser application/json'
                }), 400

            data = request.get_json()

            if not data or 'email_content' not in data:
                return jsonify({
                    'error': 'Campo email_content é obrigatório'
                }), 400

            email_content = data['email_content']

            if not isinstance(email_content, str):
                return jsonify({
                    'error': 'email_content deve ser uma string'
                }), 400

            # Process email
            logger.info("Processing email classification request")
            result = self._email_service.process_email(email_content)

            # Return successful response
            response_data = {
                'category': result.category.value,
                'confidence': result.confidence,
                'response': result.response,
                'word_count': result.word_count,
                'processing_time': result.processing_time,
                'keywords_found': result.keywords_found,
                'sentiment_score': result.sentiment_score,
                'timestamp': result.timestamp.isoformat() if result.timestamp else None
            }

            logger.info(
                f"Email classification completed: {result.category.value}")

            return jsonify(response_data), 200

        except InvalidEmailContentError as e:
            logger.warning(f"Invalid email content: {e}")
            return jsonify({'error': str(e)}), 400

        except EmailClassificationError as e:
            logger.error(f"Email classification error: {e}")
            return jsonify({'error': str(e)}), 422

        except Exception as e:
            logger.error(f"Unexpected error in email classification: {e}")
            return jsonify({'error': 'Erro interno no servidor'}), 500

    def classify_file(self):
        """
        Handle file classification requests.

        Expected form data:
        - file: uploaded file (PDF or TXT)

        Returns:
            JSON response with classification results
        """
        try:
            # Validate file upload
            if 'file' not in request.files:
                return jsonify({'error': 'Nenhum arquivo enviado'}), 400

            file = request.files['file']

            if file.filename == '' or file.filename is None:
                return jsonify({'error': 'Nome de arquivo vazio'}), 400

            # Check if file format is supported
            if not self._file_service.is_file_supported(file.filename):
                supported_formats = self._file_service.get_supported_formats()
                return jsonify({
                    'error': f'Formato de arquivo não suportado. Formatos suportados: {supported_formats}'
                }), 400

            # Read file data
            file_data = file.read()

            if not file_data:
                return jsonify({'error': 'Arquivo vazio'}), 400

            # Process file
            logger.info(
                f"Processing file classification request: {file.filename}")
            result = self._file_service.process_file(file_data, file.filename)

            # Return successful response
            response_data = {
                'category': result.category.value,
                'confidence': result.confidence,
                'response': result.response,
                'word_count': result.word_count,
                'processing_time': result.processing_time,
                'keywords_found': result.keywords_found,
                'sentiment_score': result.sentiment_score,
                'filename': file.filename,
                'timestamp': result.timestamp.isoformat() if result.timestamp else None
            }

            logger.info(
                f"File classification completed: {result.category.value}")
            return jsonify(response_data), 200

        except UnsupportedFileFormatError as e:
            logger.warning(f"Unsupported file format: {e}")
            return jsonify({'error': str(e)}), 400

        except FileProcessingError as e:
            logger.error(f"File processing error: {e}")
            return jsonify({'error': str(e)}), 422

        except EmailClassificationError as e:
            logger.error(f"Email classification error: {e}")
            return jsonify({'error': str(e)}), 422

        except Exception as e:
            logger.error(f"Unexpected error in file classification: {e}")
            return jsonify({'error': 'Erro ao processar arquivo'}), 500
