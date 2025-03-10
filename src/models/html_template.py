from langchain_core.pydantic_v1 import BaseModel, Field

class HtmlTemplate(BaseModel):
    html_template: str = Field(description="Html template with updated content after customization")