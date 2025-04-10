from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

# TODO : rename the variable name to be more descriptive
class HtmlTemplate:
    """Class responsible for handling HTML template manipulation"""
    def replace_placeholders(self, html_template:str, placeholders: dict) -> str:
        """Replace placeholders in template with provided values"""
        try:
            result = html_template
            for key, value in placeholders.items():
                placeholder = f"{key}"
                result = result.replace(placeholder, value)
            logger.info("Placeholders replaced successfully.")
            return result
        except Exception as e:
            logger.exception("Error replacing placeholders.")
            raise