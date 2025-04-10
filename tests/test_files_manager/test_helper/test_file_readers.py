import json
import os
import shutil
import tempfile
import pytest
from src.files_manager.helper.file_readers import JsonFileReader, TextFileReader

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    # Cleanup after tests
    shutil.rmtree(dir_path)

@pytest.fixture
def json_test_file(temp_dir):
    """Create a test JSON file"""
    json_path = os.path.join(temp_dir, "test.json")
    json_data = {"key": "value", "nested": {"key": "value"}}
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f)
    return json_path, json_data

@pytest.fixture
def text_test_file(temp_dir):
    """Create a test text file"""
    text_path = os.path.join(temp_dir, "test.txt")
    text_data = "Hello, world!\nThis is a test file."
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text_data)
    return text_path, text_data

# Tests for FileReader implementations
class TestJsonFileReader:
    def test_json_file_reader_success(self, json_test_file):
        path, expected_data = json_test_file
        reader = JsonFileReader()
        result = reader.read(path)
        assert result == expected_data
    
    def test_json_file_reader_file_not_found(self, temp_dir):
        reader = JsonFileReader()
        with pytest.raises(FileNotFoundError):
            reader.read(os.path.join(temp_dir, "nonexistent.json"))
    
    def test_json_file_reader_invalid_json(self, temp_dir):
        # Create invalid JSON file
        invalid_json_path = os.path.join(temp_dir, "invalid.json")
        with open(invalid_json_path, 'w', encoding='utf-8') as f:
            f.write("{invalid: json")
        
        reader = JsonFileReader()
        with pytest.raises(json.JSONDecodeError):
            reader.read(invalid_json_path)

class TestTextFileReader:
    def test_text_file_reader_success(self, text_test_file):
        path, expected_data = text_test_file
        reader = TextFileReader()
        result = reader.read(path)
        assert result == expected_data
    
    def test_text_file_reader_file_not_found(self, temp_dir):
        reader = TextFileReader()
        with pytest.raises(FileNotFoundError):
            reader.read(os.path.join(temp_dir, "nonexistent.txt"))