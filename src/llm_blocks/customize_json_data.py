from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from ..schemas.custom_json_output_format import custom_json_output_parser 


# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

with open(r'prompts\customize_json_data_prompt.txt', 'r') as file:
    customize_json_data_prompt = file.read()
    

def customize_json_data(business_name, business_description, json_placeholder):

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)
    
    # Prompt for gathering user information
    interaction_prompt = PromptTemplate(
        template=customize_json_data_prompt,
        partial_variables={"format_instructions": custom_json_output_parser.get_format_instructions()}
    )
    
    interaction_chain = interaction_prompt | llm | custom_json_output_parser
    
    response = interaction_chain.invoke({'json_placeholder':json_placeholder ,
                                     "business_name" : business_name ,
                                     "business_description" : business_description })

    return response['updated_json_placeholder']