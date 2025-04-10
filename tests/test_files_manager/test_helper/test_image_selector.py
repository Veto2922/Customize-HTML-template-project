import os
import random
import shutil
import tempfile
import pytest

from src.files_manager.helper.directory_manager import FileSystemDirectoryManager
from src.files_manager.helper.file_copier import FileSystemCopier
from src.files_manager.helper.image_selector import ImageSelector

# Fixtures for file operations
@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    # Cleanup after tests
    shutil.rmtree(dir_path)

@pytest.fixture
def image_dir(temp_dir):
    """Create a directory with test images"""
    img_dir = os.path.join(temp_dir, "images")
    sizes = ["small", "medium", "large"]
    os.makedirs(img_dir)
    
    # Create size directories
    for size in sizes:
        size_dir = os.path.join(img_dir, size)
        os.makedirs(size_dir)
        
        # Create test images
        for i in range(3):
            img_path = os.path.join(size_dir, f"test{i}.png")
            with open(img_path, 'w') as f:
                f.write(f"mock image data for {size}/test{i}.png")
    
    return img_dir

# Tests for ImageSelector
class TestImageSelector:
    def test_select_random_image(self, image_dir, monkeypatch):
        directory_manager = FileSystemDirectoryManager()
        file_copier = FileSystemCopier()
        selector = ImageSelector(directory_manager, file_copier)
        
        # Mock random.choice to return a predictable result
        monkeypatch.setattr(random, 'choice', lambda x: x[0])
        
        result = selector.select_random_image(
            os.path.join(image_dir, "small"), 
            ['.png']
        )
        
        assert result == "test0.png"
    
    def test_select_random_image_no_images(self, temp_dir):
        directory_manager = FileSystemDirectoryManager()
        file_copier = FileSystemCopier()
        selector = ImageSelector(directory_manager, file_copier)
        
        empty_dir = os.path.join(temp_dir, "empty")
        os.makedirs(empty_dir)
        
        with pytest.raises(ValueError):
            selector.select_random_image(empty_dir, ['.png'])