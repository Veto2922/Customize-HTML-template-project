from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


# Define your desired data structure.
class CustomJsonOutputFormat(BaseModel):
    updated_json_placeholder: dict = Field(description="updated json data")
    
    
custom_json_output_parser = JsonOutputParser(pydantic_object=CustomJsonOutputFormat)