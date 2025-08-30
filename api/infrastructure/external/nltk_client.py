"""
NLTK client implementation.
Handles NLTK resource management and initialization.
"""
import logging
import nltk
from typing import List

logger = logging.getLogger(__name__)


class NLTKClient:
    """
    Client for NLTK resource management.
    Encapsulates all NLTK-specific operations and resource downloads.
    """
    
    def __init__(self):
        """Initialize NLTK client"""
        self._required_resources = [
            'punkt',
            'stopwords', 
            'wordnet',
            'averaged_perceptron_tagger'
        ]
        self._initialize_resources()
    
    def _initialize_resources(self) -> None:
        """Download and initialize required NLTK resources"""
        for resource in self._required_resources:
            try:
                nltk.download(resource, quiet=True)
                logger.debug(f"NLTK resource '{resource}' downloaded successfully")
            except Exception as e:
                logger.warning(f"Failed to download NLTK resource '{resource}': {e}")
    
    def get_stopwords(self, languages: List[str]) -> set:
        """
        Get stopwords for specified languages.
        
        Args:
            languages: List of language codes
            
        Returns:
            Set of stopwords
        """
        try:
            from nltk.corpus import stopwords
            all_stopwords = set()
            
            for language in languages:
                try:
                    words = stopwords.words(language)
                    all_stopwords.update(words)
                    logger.debug(f"Loaded {len(words)} stopwords for language '{language}'")
                except Exception as e:
                    logger.warning(f"Failed to load stopwords for language '{language}': {e}")
            
            return all_stopwords
            
        except Exception as e:
            logger.error(f"Failed to load stopwords: {e}")
            return set()
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text using NLTK.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        try:
            from nltk.tokenize import word_tokenize
            return word_tokenize(text)
        except Exception as e:
            logger.warning(f"NLTK tokenization failed, using simple split: {e}")
            return text.split()
    
    def get_stemmer(self):
        """Get Porter stemmer instance"""
        try:
            from nltk.stem import PorterStemmer
            return PorterStemmer()
        except Exception as e:
            logger.error(f"Failed to get stemmer: {e}")
            return None
    
    def get_lemmatizer(self):
        """Get WordNet lemmatizer instance"""
        try:
            from nltk.stem import WordNetLemmatizer
            return WordNetLemmatizer()
        except Exception as e:
            logger.error(f"Failed to get lemmatizer: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if NLTK is properly configured"""
        try:
            # Test basic functionality
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            
            # Try a simple operation
            word_tokenize("test")
            stopwords.words('english')
            
            return True
            
        except Exception as e:
            logger.error(f"NLTK availability check failed: {e}")
            return False
