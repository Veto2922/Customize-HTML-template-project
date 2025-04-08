# llm_processor_base.py
from abc import ABC, abstractmethod

class LLMProcessor(ABC):
    @abstractmethod
    def load_model(self):
        pass
    @abstractmethod
    def load_prompt(self, prompt_path: str):
        pass

    @abstractmethod
    def build_chain(self):
        pass

    @abstractmethod
    def run(self, inputs: dict):
        pass
