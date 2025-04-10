import pytest

from src.files_manager.helper.html_template import HtmlTemplate

# Tests for template handling
class TestHtmlTemplate:
    def test_replace_placeholders(self):
        template_engine = HtmlTemplate()
        template = "Hello, {{NAME}}! Welcome to {{PLACE}}."
        placeholders = {
            "{{NAME}}": "John",
            "{{PLACE}}": "Testland"
        }
        
        result = template_engine.replace_placeholders(template, placeholders)
        
        assert result == "Hello, John! Welcome to Testland."
    
    def test_replace_placeholders_multiple_occurrences(self):
        template_engine = HtmlTemplate()
        template = "{{REPEAT}} once, {{REPEAT}} twice."
        placeholders = {
            "{{REPEAT}}": "Echo"
        }
        
        result = template_engine.replace_placeholders(template, placeholders)
        
        assert result == "Echo once, Echo twice."
    
    def test_replace_placeholders_no_match(self):
        template_engine = HtmlTemplate()
        template = "Hello, {{NAME}}!"
        placeholders = {
            "{{OTHER}}": "Value"
        }
        
        result = template_engine.replace_placeholders(template, placeholders)
        
        assert result == "Hello, {{NAME}}!"  # Unchanged