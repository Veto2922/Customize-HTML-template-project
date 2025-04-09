# llm_processor_base.py
from abc import ABC, abstractmethod

class LLMProcessor(ABC):
    @abstractmethod
    def run(self, inputs: dict):
        pass
