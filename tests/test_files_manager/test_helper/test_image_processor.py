import json
import os
import random
import shutil
import tempfile
import pytest

from src.files_manager.helper.directory_manager import FileSystemDirectoryManager
from src.files_manager.helper.file_copier import FileSystemCopier
from src.files_manager.helper.image_processor import ImagePlaceholderProcessor
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
def html_test_file(temp_dir):
    """Create a test HTML template file with placeholders"""
    html_path = os.path.join(temp_dir, "template.html")
    html_data = """<!DOCTYPE html>
    <html>
    <head>
        <title>{{TITLE}}</title>
    </head>
    <body>
        <h1>{{HEADER}}</h1>
        <p>{{CONTENT}}</p>
        <img src={{IMAGE1}}>
        <img src={{IMAGE2}}>
    </body>
    </html>"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_data)
    return html_path, html_data

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

@pytest.fixture
def image_placeholders_file(temp_dir):
    """Create an image placeholders JSON file"""
    json_path = os.path.join(temp_dir, "image_placeholders.json")
    json_data = {
        "{{IMAGE1}}": {"size": "small"},
        "{{IMAGE2}}": {"size": "medium"}
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f)
    return json_path, json_data


# Tests for ImagePlaceholderProcessor
class TestImagePlaceholderProcessor:
    def test_process_image_placeholders(self, temp_dir, html_test_file, image_dir, image_placeholders_file, monkeypatch):
        # Set up dependencies
        directory_manager = FileSystemDirectoryManager()
        file_copier = FileSystemCopier()
        image_selector = ImageSelector(directory_manager, file_copier)
        processor = ImagePlaceholderProcessor(image_selector, directory_manager)
        
        # Get test files
        _, html_content = html_test_file
        _, img_placeholders = image_placeholders_file
        
        # Set up destination directory
        dest_folder = os.path.join(temp_dir, "assets/img/temp")
        
        # Mock random.choice to make the test deterministic
        monkeypatch.setattr(random, 'choice', lambda x: x[0])
        
        # Process the placeholders
        result = processor.process_image_placeholders(
            html_content, 
            img_placeholders,
            image_dir,
            dest_folder
        )
        
        # Check results
        assert '"assets/img/temp/test0.png"' in result
        assert os.path.exists(os.path.join(dest_folder, "test0.png"))
        
        # Original placeholders should be replaced
        assert "{{IMAGE1}}" not in result
        assert "{{IMAGE2}}" not in result