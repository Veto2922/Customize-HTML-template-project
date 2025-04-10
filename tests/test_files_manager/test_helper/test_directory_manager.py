import os
import shutil
import pytest
import tempfile
from src.files_manager.helper.directory_manager import FileSystemDirectoryManager

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    # Cleanup after tests
    shutil.rmtree(dir_path)

# Tests for DirectoryManager implementations
class TestFileSystemDirectoryManager:

    def test_ensure_directory_exists_create(self, temp_dir):
        manager = FileSystemDirectoryManager()
        new_dir = os.path.join(temp_dir, "new_directory")
        
        result = manager.ensure_directory_exists(new_dir)
        
        assert result is True
        assert os.path.exists(new_dir)
        assert os.path.isdir(new_dir)
    
    def test_ensure_directory_exists_already_exists(self, temp_dir):
        manager = FileSystemDirectoryManager()
        
        # Directory already exists
        result = manager.ensure_directory_exists(temp_dir)
        
        assert result is True
    
    def test_list_files_with_extensions(self, temp_dir):
        manager = FileSystemDirectoryManager()
        
        # Create test files with different extensions
        extensions = ['.txt', '.jpg', '.png']
        expected_files = []
        
        for ext in extensions:
            for i in range(2):
                filename = f"file{i}{ext}"
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(f"test content for {filename}")
                if ext in ['.jpg', '.png']:
                    expected_files.append(filename)
        
        # Also create some non-matching files
        with open(os.path.join(temp_dir, "file.pdf"), 'w') as f:
            f.write("pdf content")
        
        # Get files with specific extensions
        result = manager.list_files_with_extensions(temp_dir, ['.jpg', '.png'])
        
        # Check results
        assert sorted(result) == sorted(expected_files)
    
    def test_list_files_directory_not_found(self, temp_dir):
        manager = FileSystemDirectoryManager()
        nonexistent_dir = os.path.join(temp_dir, "nonexistent")
        
        with pytest.raises(FileNotFoundError):
            manager.list_files_with_extensions(nonexistent_dir, ['.txt'])
