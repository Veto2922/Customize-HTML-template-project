import os
from typing import Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.providers.base import LLMProvider

class GoogleLLMProvider(LLMProvider):
    """Concrete implementation for Google's Generative AI"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash", api_key: Optional[str] = None):
        self._model_name = model_name
        self._api_key = api_key
        self._llm = None
        
    def initialize_llm(self):
        """Initialize the Google Generative AI model"""
        if not self._api_key:
            load_dotenv()
            self._api_key = os.getenv("GEMINI_API_KEY")
            
        if not self._api_key:
            raise ValueError("Google API key not found. Please provide it or set GEMINI_API_KEY in environment.")
            
        self._llm = ChatGoogleGenerativeAI(
            model=self._model_name, 
            google_api_key=self._api_key,
            temperature=0,
        )
        
    @property
    def llm(self):
        """Return the initialized LLM instance"""
        if not self._llm:
            self.initialize_llm()
        return self._llm