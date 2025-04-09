from abc import ABC, abstractmethod

class BaseLLMComponent(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses.
        """
        pass