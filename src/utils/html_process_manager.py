import os
import json
from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

class HtmlProcessManager:
    def __init__(self):
        logger.info("HtmlProcessManager initialized.")

    def generate_new_html(self, new_json_placeholder, html_placeholder):
        try:
            for key, value in new_json_placeholder.items():
                placeholder = f"{key}"
                html_placeholder = html_placeholder.replace(placeholder, value)
            logger.info("New HTML generated successfully.")
            return html_placeholder
        except Exception as e:
            logger.exception("Error generating new HTML.")
            raise

    def save_new_html(self, new_html, save_path):
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(new_html)
            logger.info("HTML saved to: %s", save_path)
        except Exception as e:
            logger.exception("Failed to save new HTML to %s", save_path)
            raise

    def get_json_placeholder(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                json_placeholder = json.load(file)
            logger.info("JSON placeholder loaded from: %s", path)
            return json_placeholder
        except FileNotFoundError:
            logger.error("JSON file not found at path: %s", path)
            raise
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from: %s", path)
            raise
        except Exception as e:
            logger.exception("Unexpected error loading JSON placeholder.")
            raise

    def get_html_placeholder(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                html_placeholder = file.read()
            logger.info("HTML placeholder loaded from: %s", path)
            return html_placeholder
        except FileNotFoundError:
            logger.error("HTML file not found at path: %s", path)
            raise
        except Exception as e:
            logger.exception("Unexpected error loading HTML placeholder.")
            raise
