from langchain_core.prompts import ChatPromptTemplate
from src.templates.base import TemplateBuilder

class HtmlCustomizationTemplateBuilder(TemplateBuilder):
    """Template builder for HTML customization prompts"""
    
    def __init__(self, format_instructions: str):
        self._format_instructions = format_instructions
        
    def build_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template("""
**Act as an expert HTML developer and content strategist.**  
You have extensive experience in web development and content customization, specializing in dynamically adapting HTML templates based on user preferences.  

### **Objective:**  
Your task is to analyze a given HTML template and modify its **text content** based on the responses provided by the user. The goal is to ensure that the final HTML output accurately reflects the user's preferences while maintaining structural integrity and proper formatting.  

### **Process:**  
1. **Analyze User Inputs:**  
   - Carefully examine the provided **questions and user responses** to understand their content preferences.  
   - Identify key phrases, themes, and context to determine what changes need to be applied to the template.  

2. **Modify the HTML Template:**  
   - Update **only the text content** within the template while preserving the existing HTML structure, including elements, attributes, and styles.  
   - Ensure that text replacements maintain coherence and proper alignment with the template's purpose.  
   - If any user input is unclear or missing, generate a reasonable default response that aligns with the context.  

3. **Ensure Readability & Formatting:**  
   - Maintain proper text spacing, line breaks, and formatting conventions.  
   - If necessary, adjust the HTML markup to improve readability without altering functionality.  

4. **Output the Updated HTML Template:**  
   - Provide the final modified HTML code while keeping the structure intact.  
   - Ensure that all user preferences are accurately reflected in the text content.  

### **Inputs:**  
#### **HTML Template:**  
```html  
{html_template}  
```  

#### **Questions and User Responses:**  
{Q_A_list}  

### **Expected Output:**  
A fully updated HTML template with text content modified according to the user's answers, ensuring clarity, relevance, and consistency.  
Your html code should be start with body <body> tag and end with body tag </body>.
please answer in json like below:
```json
{{
  "html_template": "<body>Updated HTML code here...</body>"
}}
```

{format_instructions}

Take a deep breath and work on this problem step by step.  
""",
partial_variables={"format_instructions": self._format_instructions}
)