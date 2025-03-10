from langchain_core.prompts import ChatPromptTemplate
from src.templates.base import TemplateBuilder

class HtmlAnalysisTemplateBuilder(TemplateBuilder):
    """Template builder for HTML analysis prompts"""
    
    def build_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template("""
                **Act as an expert HTML developer and content strategist.** Your role is to generate a precise and comprehensive list of key questions that a user should answer in order to fully customize the **text content** of an HTML template.  

                ### **Instructions:**  
                1. **Analyze the provided HTML template:**  
                - Identify all text-based elements, including headings, paragraphs, buttons, navigation links, form placeholders, and any other textual content.  
                - Exclude non-text elements such as images, colors, fonts, and layout settings.  

                2. **Generate key questions:**  
                - Focus only on **text-related customization** (e.g., wording, tone, branding consistency, and localization).  
                - Ensure the questions guide the user in making informed choices about the **tone, clarity, and structure** of the content.  

                3. **Organize the questions logically:**  
                - Begin with general content structure (e.g., page headings and main text) and move to specific elements (e.g., button labels and form placeholders).  
                - Cover both **static text** (like headings and paragraphs) and **interactive text** (like form labels and call-to-action buttons).  

                4. **Limit the output to exactly 10 questions.**  

                ### **HTML Template:**  
                ```html
                {html_template}
                ```  

                ### **Output Format:**  
                - Provide the questions in a **single-line, comma-separated format**, without any additional text.  
                - Example output:  
                ```
                1. What should be the main heading of the page?, 2. What introductory text should appear in the hero section?, 3. What should the call-to-action button say?, ...etc
                ```

                IMPORTANT: Do not use commas (,) inside your questions, as I am using CommaSeparatedListOutputParser. Instead, use a dash (-) to separate elements within a question.

                **Take a deep breath and work on this problem step by step.**  
                """)