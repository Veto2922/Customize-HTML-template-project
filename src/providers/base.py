from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def initialize_llm(self):
        """Initialize the LLM with appropriate credentials"""
        pass
    
    @property
    @abstractmethod
    def llm(self):
        """Return the initialized LLM instance"""
        pass