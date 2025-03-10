from src.providers.google_provider import GoogleLLMProvider
from src.parsers.comma_parser import CommaSeparatedParser
from src.parsers.json_parser import JsonParser
from src.templates.html_analysis import HtmlAnalysisTemplateBuilder
from src.templates.html_customization import HtmlCustomizationTemplateBuilder
from src.models.html_template import HtmlTemplate
from src.processor import LangChainProcessor

def main():
    # Initialize the LLM provider
    llm_provider = GoogleLLMProvider()
    
    # Create the processor
    processor = LangChainProcessor(llm_provider)
    
    # Load HTML content
    processor.load_html_from_file(r'data\test_html.html')
    
    # Generate questions
    template_builder = HtmlAnalysisTemplateBuilder()
    parser = CommaSeparatedParser()
    
    questions = processor.generate_questions(template_builder, parser)
    print("Generated Questions:")
    for idx, question in enumerate(questions, 1):
        print(f"{idx}. {question}")
    
    # -------------------------------------------------
    # Example QA responses
    website_content = {
        "What is the desired brand name- logo text for the website header and footer?": "TechNova",
        "What wording should be used for the main heading (H1) on the hero section of the landing page?": "Revolutionizing Your Digital Experience",
        "What descriptive text should accompany the main heading in the hero section to explain the business offering?": "Empower your business with cutting-edge solutions designed to streamline operations and maximize efficiency.",
        "What call-to-action text should be used on the primary button in the hero section?": "Get Started Today",
        "What heading should be used for the 'Features' section to best describe the benefits offered?": "Why Choose TechNova?",
        "What wording should be used for each of the individual feature titles- for example- Smart Automation- Advanced Analytics- Enterprise Security?": [
            "Smart Automation",
            "Advanced Analytics",
            "Enterprise Security",
            "Seamless Integration"
        ],
        "What wording should be used for the 'Testimonials' section heading to convey customer satisfaction?": "What Our Clients Say",
        "What is the desired wording for the call-to-action heading and supporting text in the email collection section?": {
            "heading": "Stay Updated with Our Latest Innovations",
            "text": "Subscribe to our newsletter for exclusive insights, updates, and special offers."
        },
        "What placeholder text should be used in the email input field of the email collection form?": "Abdelrahman.m2922@gmail.com",
        "What wording should be used for the navigation links (e.g.- Features- Testimonials- Pricing- Contact)?": [
            "Features",
            "Testimonials",
            "Pricing",
            "Contact"
        ]
    }
    
    # Customize HTML with responses
    json_parser = JsonParser(HtmlTemplate)
    customization_builder = HtmlCustomizationTemplateBuilder(json_parser.get_format_instructions())
    
    customized_html = processor.customize_html(
        customization_builder,
        json_parser,
        website_content
    )
    
    print("\nCustomized HTML Template:")
    print(customized_html['html_template'])

if __name__ == "__main__":
    main()