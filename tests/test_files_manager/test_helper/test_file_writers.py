import os
import shutil
import tempfile
import pytest

from src.files_manager.helper.file_writers import TextFileWriter

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    # Cleanup after tests
    shutil.rmtree(dir_path)

# Tests for FileWriter implementations
class TestTextFileWriter:
    def test_text_file_writer_success(self, temp_dir):
        writer = TextFileWriter()
        test_content = "Test content to write"
        output_path = os.path.join(temp_dir, "output.txt")
        
        writer.write(test_content, output_path)
        
        # Verify file was written correctly
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == test_content
