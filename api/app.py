import os
import logging
from flask import Flask
from flask_cors import CORS
from container import DIContainer
from core.config import AppConfig
from core.error_handlers import register_error_handlers

# Configure logging
logging.basicConfig(
    level=getattr(logging, AppConfig.LOG_LEVEL),
    format=AppConfig.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Initialize dependency injection container
container = DIContainer()


def create_app() -> Flask:
    """
    Application factory function that creates and configures the Flask application.
    Uses dependency injection to wire up all components.

    Returns:
        Configured Flask application
    """
    try:
        # Initialize the dependency injection container
        container.initialize()

        # Get controller instances from container
        email_controller = container.get_email_controller()

        # Register centralized error handlers
        register_error_handlers(app)

        # Register routes with controllers
        register_routes(email_controller)

        logger.info(
            "Flask application created successfully with new architecture")
        return app

    except Exception as e:
        logger.error(f"Failed to create Flask application: {e}")
        raise


def register_routes(email_controller) -> None:
    """
    Register all application routes with their respective controllers.

    Args:
        email_controller: Controller for email-related endpoints
        health_controller: Controller for health check endpoints
    """

    # Email processing routes
    app.route('/api/classify', methods=['POST']
              )(email_controller.classify_email)
    app.route('/api/classify-file',
              methods=['POST'])(email_controller.classify_file)


def initialize_application() -> None:
    """
    Initialize the application and all its components.
    This function should be called before starting the server.
    """
    try:
        # Validate configuration
        AppConfig.validate_config()

        # Create model cache directory
        os.makedirs(AppConfig.MODEL_CACHE_DIR, exist_ok=True)

        # Initialize the application
        create_app()

        logger.info("Application initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise


initialize_application()


if __name__ == '__main__':
    """
    Main entry point for the application.
    Initializes the application and starts the Flask development server.
    """
    try:
        app.run(
            debug=AppConfig.DEBUG,
            host=AppConfig.HOST,
            port=AppConfig.PORT
        )

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        exit(1)
