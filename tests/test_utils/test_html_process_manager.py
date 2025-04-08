import pytest
import json
from unittest import mock
from src.Log_Manager.log_manager import get_logger
from src.utils.html_process_manager import HtmlProcessManager  # Adjust the import path as necessary

logger = get_logger(__name__)

class TestHtmlProcessManager:
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='{"key": "value"}')
    def test_get_json_placeholder(self, mock_open):
        manager = HtmlProcessManager()
        result = manager.get_json_placeholder("fake_path.json")
        assert result == {"key": "value"}
        mock_open.assert_called_once_with("fake_path.json", 'r', encoding='utf-8')

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_save_new_html(self, mock_open):
        manager = HtmlProcessManager()
        manager.save_new_html("<html>New Content</html>", "fake_path.html")
        mock_open.assert_called_once_with("fake_path.html", 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with("<html>New Content</html>")

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='<html>{{key}}</html>')
    def test_generate_new_html(self, mock_open):
        manager = HtmlProcessManager()
        new_json_placeholder = {"c100": "value"}
        html_placeholder = "<html>c100</html>"
        result = manager.generate_new_html(new_json_placeholder, html_placeholder)
        assert result == "<html>value</html>"

    @mock.patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_json_placeholder_file_not_found(self, mock_open):
        manager = HtmlProcessManager()
        with pytest.raises(FileNotFoundError):
            manager.get_json_placeholder("non_existent_file.json")

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='not a json')
    def test_get_json_placeholder_json_decode_error(self, mock_open):
        manager = HtmlProcessManager()
        with pytest.raises(json.JSONDecodeError):
            manager.get_json_placeholder("fake_path.json")

    @mock.patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_html_placeholder_file_not_found(self, mock_open):
        manager = HtmlProcessManager()
        with pytest.raises(FileNotFoundError):
            manager.get_html_placeholder("non_existent_file.html")

