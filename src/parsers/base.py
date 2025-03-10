from abc import ABC, abstractmethod

class OutputParser(ABC):
    """Abstract base class for output parsers"""
    
    @abstractmethod
    def get_parser(self):
        """Return the appropriate parser for the task"""
        pass