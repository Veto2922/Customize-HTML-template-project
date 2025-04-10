import os
import shutil
import tempfile
import pytest

from src.files_manager.helper.file_copier import FileSystemCopier

# Fixtures for file operations
@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    # Cleanup after tests
    shutil.rmtree(dir_path)

@pytest.fixture
def text_test_file(temp_dir):
    """Create a test text file"""
    text_path = os.path.join(temp_dir, "test.txt")
    text_data = "Hello, world!\nThis is a test file."
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text_data)
    return text_path, text_data

# Tests for FileCopier implementations
class TestFileSystemCopier:
    def test_file_system_copier_success(self, text_test_file, temp_dir):
        source_path, _ = text_test_file
        dest_path = os.path.join(temp_dir, "copied.txt")
        
        copier = FileSystemCopier()
        copier.copy(source_path, dest_path)
        
        # Verify file was copied
        assert os.path.exists(dest_path)
        with open(source_path, 'r') as src, open(dest_path, 'r') as dst:
            assert src.read() == dst.read()
    
    def test_file_system_copier_source_not_found(self, temp_dir):
        copier = FileSystemCopier()
        with pytest.raises(FileNotFoundError):
            copier.copy(
                os.path.join(temp_dir, "nonexistent.txt"),
                os.path.join(temp_dir, "dest.txt")
            )