from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from src.parsers.base import OutputParser

class JsonParser(OutputParser):
    """Concrete implementation for JSON output parser"""
    
    def __init__(self, model_class: BaseModel):
        self._model_class = model_class
        
    def get_parser(self):
        return JsonOutputParser(pydantic_object=self._model_class)
    
    def get_format_instructions(self):
        return self.get_parser().get_format_instructions()