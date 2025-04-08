# customize_json_processor.py
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from base import LLMProcessor
from schemas.custom_json_output_format import custom_json_output_parser
import os
from dotenv import load_dotenv



class CustomizeJsonPlaceholder(LLMProcessor):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(f"API key not found in environment variable: GEMINI_API_KEY")

    def load_model(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=self.api_key)
        
    def load_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'customize_json_data_prompt.txt')
        with open(prompt_path, 'r' , encoding='utf-8') as file:
            self.customize_json_data_prompt = file.read()

    def build_chain(self):
        prompt = PromptTemplate(
            template=self.customize_json_data_prompt,
            partial_variables={"format_instructions": custom_json_output_parser.get_format_instructions()}
        )
        self.chain = prompt | self.llm | custom_json_output_parser

    def run(self, business_name : str, business_description : str , json_placeholder : str):
        self.load_model()
        self.load_prompt()
        self.build_chain()
        
        if not self.chain:
            raise ValueError("Chain is not built. Call build_chain() first.")
        
        
        response = self.chain.invoke({
            'json_placeholder': json_placeholder,
            'business_name': business_name,
            'business_description': business_description
        })
        return response['updated_json_placeholder']
    
    
if __name__ == "__main__":
    customize_json_processor = CustomizeJsonPlaceholder()
    updated_json = customize_json_processor.run(
        business_name="My Business",
        business_description="A description of my business",
        json_placeholder='{"business name": "value"}'
    )
    print(updated_json)


