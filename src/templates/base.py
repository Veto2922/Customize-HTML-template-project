from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate

class TemplateBuilder(ABC):
    """Abstract base class for template builders"""
    
    @abstractmethod
    def build_template(self) -> ChatPromptTemplate:
        """Build and return the prompt template"""
        pass