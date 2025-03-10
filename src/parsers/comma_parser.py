from langchain_core.output_parsers import CommaSeparatedListOutputParser
from src.parsers.base import OutputParser

class CommaSeparatedParser(OutputParser):
    """Concrete implementation for comma-separated list parser"""
    
    def get_parser(self):
        return CommaSeparatedListOutputParser()