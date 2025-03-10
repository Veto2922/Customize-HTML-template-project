from typing import Dict, Any, List
from src.providers.base import LLMProvider
from src.templates.base import TemplateBuilder
from src.parsers.base import OutputParser

class LangChainProcessor:
    """Main processor class that combines all components"""
    
    def __init__(self, llm_provider: LLMProvider):
        self._llm_provider = llm_provider
        self._html_content = None
        
    def load_html_from_file(self, file_path: str) -> str:
        """Load HTML content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:  # Specify UTF-8 encoding
                self._html_content = f.read()
            return self._html_content
        except Exception as e:
            raise IOError(f"Failed to load HTML file: {e}")

    
    def set_html_content(self, html_content: str):
        """Set HTML content directly"""
        self._html_content = html_content
        
    def generate_questions(self, template_builder: TemplateBuilder, output_parser: OutputParser) -> List[str]:
        """Generate questions for HTML customization"""
        if not self._html_content:
            raise ValueError("HTML content is not set. Please load or set HTML content first.")
            
        prompt = template_builder.build_template()
        parser = output_parser.get_parser()
        
        chain = prompt | self._llm_provider.llm | parser
        
        response = chain.invoke({
            'html_template': self._html_content
        })
        
        return response
    
    def customize_html(self, 
                      template_builder: TemplateBuilder,
                      output_parser: OutputParser,
                      qa_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Customize HTML based on question-answer pairs"""
        if not self._html_content:
            raise ValueError("HTML content is not set. Please load or set HTML content first.")
            
        prompt = template_builder.build_template()
        parser = output_parser.get_parser()
        
        chain = prompt | self._llm_provider.llm | parser
        
        response = chain.invoke({
            'html_template': self._html_content,
            'Q_A_list': qa_responses
        })
        
        return response