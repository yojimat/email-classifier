"""
Dependency injection container for the email classification system.
Manages the creation and wiring of all application components 
"""
import logging
from typing import Optional

# Repository imports
from infrastructure.repositories.config_repository import ConfigRepository
from infrastructure.repositories.model_repository import ModelRepository
from infrastructure.repositories.file_repository import FileRepository
from infrastructure.repositories.external_service_repository import ExternalServiceRepository

# Service imports
from services.preprocessing_service import TextPreprocessingService
from services.feature_extraction_service import FeatureExtractionService
from services.classification_service import ClassificationService
from services.response_service import ResponseGenerationService
from services.email_service import EmailProcessingService
from services.file_processing_service import FileProcessingService
from services.external_ai_service import ExternalAIService

# Controller imports
from controllers.email_controller import EmailController

# Core imports
from core.interfaces.repositories import (
    IConfigRepository, IModelRepository, IFileRepository, IExternalServiceRepository
)
from core.interfaces.services import (
    ITextPreprocessingService, IFeatureExtractionService, IClassificationService,
    IResponseGenerationService, IEmailProcessingService, IFileProcessingService,
    IExternalAIService
)

logger = logging.getLogger(__name__)


class DIContainer:
    def __init__(self):
        """Initialize the DI container"""
        self._repositories = {}
        self._services = {}
        self._controllers = {}
        self._initialized = False

    def initialize(self) -> None:
        """
        Initialize all components in the correct order.
        This method should be called once during application startup.
        """
        if self._initialized:
            logger.warning("Container already initialized")
            return

        try:
            logger.info("Initializing dependency injection container")

            self._initialize_repositories()

            # Initialize services (depend on repositories)
            self._initialize_services()

            # Initialize controllers (depend on services)
            self._initialize_controllers()

            self._initialized = True
            logger.info(
                "Dependency injection container initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize DI container: {e}")
            raise

    def _initialize_repositories(self) -> None:
        """Initialize all repository instances"""
        logger.debug("Initializing repositories")

        self._repositories['config'] = ConfigRepository()
        self._repositories['model'] = ModelRepository()
        self._repositories['file'] = FileRepository()
        self._repositories['external_service'] = ExternalServiceRepository()

        logger.debug("Repositories initialized")

    def _initialize_services(self) -> None:
        """Initialize all service instances with their dependencies"""
        logger.debug("Initializing services")

        config_repo = self._repositories['config']
        model_repo = self._repositories['model']
        file_repo = self._repositories['file']
        external_service_repo = self._repositories['external_service']

        self._services['preprocessing'] = TextPreprocessingService(config_repo)

        self._services['feature_extraction'] = FeatureExtractionService(
            config_repo)

        self._services['classification'] = ClassificationService(
            model_repo, config_repo)

        # External AI service (optional)
        external_ai_service = None
        if external_service_repo.is_openai_configured():
            external_ai_service = ExternalAIService(external_service_repo)
            self._services['external_ai'] = external_ai_service

        # Response generation service
        self._services['response'] = ResponseGenerationService(
            external_ai_service)

        # Main email processing service (orchestrator)
        self._services['email_processing'] = EmailProcessingService(
            self._services['preprocessing'],
            self._services['feature_extraction'],
            self._services['classification'],
            self._services['response']
        )

        # File processing service
        self._services['file_processing'] = FileProcessingService(
            file_repo,
            self._services['email_processing']
        )

        logger.debug("Services initialized")

    def _initialize_controllers(self) -> None:
        logger.debug("Initializing controllers")

        # Email controller
        self._controllers['email'] = EmailController(
            self._services['email_processing'],
            self._services['file_processing']
        )

        logger.debug("Controllers initialized")

    # Repository getters
    def get_config_repository(self) -> IConfigRepository:
        """Get configuration repository instance"""
        self._ensure_initialized()
        return self._repositories['config']

    def get_model_repository(self) -> IModelRepository:
        """Get model repository instance"""
        self._ensure_initialized()
        return self._repositories['model']

    def get_file_repository(self) -> IFileRepository:
        """Get file repository instance"""
        self._ensure_initialized()
        return self._repositories['file']

    def get_external_service_repository(self) -> IExternalServiceRepository:
        """Get external service repository instance"""
        self._ensure_initialized()
        return self._repositories['external_service']

    # Service getters
    def get_preprocessing_service(self) -> ITextPreprocessingService:
        """Get text preprocessing service instance"""
        self._ensure_initialized()
        return self._services['preprocessing']

    def get_feature_extraction_service(self) -> IFeatureExtractionService:
        """Get feature extraction service instance"""
        self._ensure_initialized()
        return self._services['feature_extraction']

    def get_classification_service(self) -> IClassificationService:
        """Get classification service instance"""
        self._ensure_initialized()
        return self._services['classification']

    def get_response_service(self) -> IResponseGenerationService:
        """Get response generation service instance"""
        self._ensure_initialized()
        return self._services['response']

    def get_email_processing_service(self) -> IEmailProcessingService:
        """Get email processing service instance"""
        self._ensure_initialized()
        return self._services['email_processing']

    def get_file_processing_service(self) -> IFileProcessingService:
        """Get file processing service instance"""
        self._ensure_initialized()
        return self._services['file_processing']

    def get_external_ai_service(self) -> Optional[IExternalAIService]:
        """Get external AI service instance (may be None if not configured)"""
        self._ensure_initialized()
        return self._services.get('external_ai')

    # Controller getters
    def get_email_controller(self) -> EmailController:
        """Get email controller instance"""
        self._ensure_initialized()
        return self._controllers['email']

    def _ensure_initialized(self) -> None:
        """Ensure the container is initialized"""
        if not self._initialized:
            raise RuntimeError(
                "DI Container not initialized. Call initialize() first.")
