"""
Response generation service implementation.
Handles response generation operations following the Single Responsibility Principle.
"""
import logging
from typing import List, Optional
from core.interfaces.services import IResponseGenerationService, IExternalAIService
from core.domain.models import ClassificationResult, EmailFeatures, EmailCategory
from core.domain.exceptions import ResponseGenerationError

logger = logging.getLogger(__name__)


class ResponseGenerationService(IResponseGenerationService):
    """
    Service responsible for generating email responses.
    Follows Single Responsibility Principle by focusing only on response generation.
    """

    def __init__(self, external_ai_service: Optional[IExternalAIService] = None):
        """
        Initialize the response generation service.

        Args:
            external_ai_service: Optional external AI service for advanced response generation
        """
        self._external_ai_service = external_ai_service

    def generate_response(self, original_text: str, classification: ClassificationResult, features: EmailFeatures) -> str:
        """
        Generate appropriate response based on classification.

        Args:
            original_text: Original email text
            classification: Classification result
            features: Email features

        Returns:
            Generated response text
        """
        try:
            # Try external AI service first if available
            if self._external_ai_service and self._external_ai_service.is_available():
                try:
                    ai_response = self._external_ai_service.generate_ai_response(
                        original_text, classification.category
                    )
                    if ai_response:
                        logger.info(
                            "Generated response using external AI service")
                        return ai_response
                except Exception as e:
                    logger.warning(
                        f"External AI service failed, using templates: {e}")

            # Fallback to template-based response
            return self._generate_template_response(classification.category, features)

        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            raise ResponseGenerationError(
                f"Failed to generate response: {str(e)}")

    def _generate_template_response(self, category: EmailCategory, features: EmailFeatures) -> str:
        """
        Generate response using predefined templates.

        Args:
            category: Email category
            features: Email features

        Returns:
            Template-based response
        """
        if category == EmailCategory.PRODUCTIVE:
            return self._generate_productive_response(features)
        else:
            return self._generate_unproductive_response(features)

    def _generate_productive_response(self, features: EmailFeatures) -> str:
        """
        Generate response for productive emails.

        Args:
            features: Email features

        Returns:
            Response for productive email
        """
        templates = [
            """Prezado(a),

Agradeço pelo seu email. Li atentamente os pontos apresentados e considero muito relevantes para nosso contexto atual.

{context}

Sugiro agendarmos uma reunião para discutirmos os próximos passos e alinharmos as expectativas. 
Fico no aguardo de sua disponibilidade.

Atenciosamente""",

            """Olá,

Obrigado por compartilhar estas informações importantes. 

{context}

Vou analisar os detalhes e retornarei com um feedback mais estruturado até o final do dia.
Caso necessite de algo urgente, por favor me avise.

Cordialmente""",

            """Prezado(a),

Recebi seu email e agradeço pelo contato. Os pontos mencionados são de grande interesse.

{context}

Gostaria de agendar uma conversa para discutirmos melhor as possibilidades de colaboração.
Quando seria um bom momento para você?

Atenciosamente"""
        ]

        # Generate context based on keywords found
        context = self._generate_context_for_productive(
            features.productive_keywords)

        # Select template based on features
        template_index = self._select_productive_template(features)
        selected_template = templates[template_index]

        return selected_template.format(context=context)

    def _generate_unproductive_response(self, features: EmailFeatures) -> str:
        """
        Generate response for unproductive emails.

        Args:
            features: Email features

        Returns:
            Response for unproductive email
        """
        templates = [
            """Olá,

Agradeço pelo contato. No momento, não tenho interesse/disponibilidade para esta proposta.

Obrigado pela compreensão.

Atenciosamente""",

            """Prezado(a),

Recebi sua mensagem. Infelizmente, não se adequa às nossas necessidades atuais.

Agradeço o contato e desejo sucesso em seus projetos.

Cordialmente""",

            """Olá,

Obrigado pelo email. Atualmente não estou buscando este tipo de oportunidade.

Desejo-lhe muito sucesso.

Atenciosamente"""
        ]

        # Select template based on features
        template_index = self._select_unproductive_template(features)
        return templates[template_index]

    def _generate_context_for_productive(self, productive_keywords: List[str]) -> str:
        """
        Generate context text based on productive keywords found.

        Args:
            productive_keywords: List of productive keywords found

        Returns:
            Context text
        """
        if not productive_keywords:
            return "Acredito que podemos trabalhar juntos para alcançar os objetivos mencionados."

        # Use first few keywords to create context
        keywords = productive_keywords[:3]

        if len(keywords) == 1:
            return f"Em relação ao ponto sobre {keywords[0]}, acredito que podemos desenvolver uma abordagem eficaz."
        elif len(keywords) == 2:
            return f"Em relação aos pontos sobre {keywords[0]} e {keywords[1]}, vejo grande potencial para colaboração."
        else:
            return f"Em relação aos pontos sobre {', '.join(keywords[:-1])} e {keywords[-1]}, acredito que podemos desenvolver uma abordagem eficaz."

    def _select_productive_template(self, features: EmailFeatures) -> int:
        """
        Select appropriate template for productive emails based on features.

        Args:
            features: Email features

        Returns:
            Template index
        """
        # More formal template for longer, more structured emails
        if features.word_count > 100 and features.productive_score > 2:
            return 0  # Most formal template
        elif features.word_count > 50:
            return 1  # Medium formality
        else:
            return 2  # Shorter, more direct

    def _select_unproductive_template(self, features: EmailFeatures) -> int:
        """
        Select appropriate template for unproductive emails based on features.

        Args:
            features: Email features

        Returns:
            Template index
        """
        # More direct rejection for obvious spam (URLs, excessive punctuation)
        if features.has_urls or features.exclamation_count > 2:
            return 1  # More direct template
        elif features.unproductive_score > 2:
            return 0  # Standard polite rejection
        else:
            return 2  # Gentle rejection
