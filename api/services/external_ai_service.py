"""
External AI service implementation.
Handles integration with external AI services like OpenAI 
"""
import logging
from openai import OpenAI
from core.interfaces.services import IExternalAIService
from core.interfaces.repositories import IExternalServiceRepository
from core.domain.models import EmailCategory
from core.domain.exceptions import ResponseGenerationError

logger = logging.getLogger(__name__)


class ExternalAIService(IExternalAIService):
    """
    Service responsible for external AI integrations.
    """

    def __init__(self, external_service_repository: IExternalServiceRepository):
        """
        Initialize the external AI service.

        Args:
            external_service_repository: Repository for external service configurations
        """
        self._external_repo = external_service_repository
        self._is_configured = False
        self._client = OpenAI()
        self._initialize_openai()

    def _initialize_openai(self) -> None:
        """Initialize OpenAI client if configured"""
        try:
            api_key = self._external_repo.get_openai_api_key()
            if api_key:
                self._client.api_key = api_key
                self._is_configured = True
                logger.info("OpenAI service initialized successfully")
            else:
                logger.info("OpenAI API key not configured")
                self._is_configured = False
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI: {e}")
            self._is_configured = False

    def generate_ai_response(self, text: str, category: EmailCategory) -> str:
        """
        Generate response using external AI service.

        Args:
            text: Email text
            category: Classification category

        Returns:
            AI-generated response

        Raises:
            ResponseGenerationError: If AI response generation fails
        """
        if not self.is_available():
            raise ResponseGenerationError(
                "External AI service is not available")

        try:
            prompt = self._create_prompt(text, category)

            response = self._client.responses.create(
                model=self._external_repo.get_openai_model_name(),
                input=[
                    {"role": "developer",
                        "content": "Você é um assistente profissional de emails."},
                    {"role": "user", "content": prompt}
                ],
                # max_tokens=self._external_repo.get_openai_max_tokens(),
                temperature=self._external_repo.get_openai_temperature()
            )

            generated_response = response.output_text.strip()
            # generated_response = response.choices[0].message.content.strip()

            if not generated_response:
                raise ResponseGenerationError("Empty response from AI service")

            logger.info("Successfully generated AI response")
            return generated_response

        except Exception as e:
            logger.error(f"AI response generation failed: {e}")
            raise ResponseGenerationError(
                f"Failed to generate AI response: {str(e)}")

    def is_available(self) -> bool:
        """Check if external AI service is available"""
        return self._is_configured and self._external_repo.is_openai_configured()

    def _create_prompt(self, text: str, category: EmailCategory) -> str:
        """
        Create appropriate prompt for AI response generation.

        Args:
            text: Email text
            category: Classification category

        Returns:
            Formatted prompt
        """
        # Limit text length to avoid token limits
        limited_text = text[:1000] if len(text) > 1000 else text

        if category == EmailCategory.PRODUCTIVE:
            prompt = f"""
            Gere uma resposta profissional e engajada para o seguinte email classificado como produtivo.
            
            Email: {limited_text}
            
            Instruções:
            - Resposta engajada e propositiva
            - Tom profissional e cordial
            - Máximo 150 palavras
            - Demonstre interesse em colaboração
            - Sugira próximos passos quando apropriado
            """
        else:
            prompt = f"""
            Gere uma resposta profissional e educada para o seguinte email classificado como improdutivo.
            
            Email: {limited_text}
            
            Instruções:
            - Resposta educada mas breve
            - Tom profissional e respeitoso
            - Máximo 100 palavras
            - Decline educadamente sem ser rude
            - Agradeça pelo contato
            """

        return prompt
