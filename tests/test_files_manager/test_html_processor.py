import json
import os
import random
import shutil
import tempfile
import pytest

from src.files_manager.helper.directory_manager import FileSystemDirectoryManager
from src.files_manager.helper.file_copier import FileSystemCopier
from src.files_manager.helper.file_readers import JsonFileReader, TextFileReader
from src.files_manager.helper.file_writers import TextFileWriter
from src.files_manager.helper.html_template import HtmlTemplate
from src.files_manager.helper.image_processor import ImagePlaceholderProcessor
from src.files_manager.helper.image_selector import ImageSelector
from src.files_manager.html_processor import HtmlProcessor

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
def json_test_file(temp_dir):
    """Create a test JSON file"""
    json_path = os.path.join(temp_dir, "test.json")
    json_data = {
                "{{TITLE}}": "Test Title",
                "{{HEADER}}": "Test Header",
                "{{CONTENT}}": "Test Content"
            }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f)
    return json_path, json_data

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
            img_path = os.path.join(size_dir, f"test{i}.jpg")
            with open(img_path, 'w') as f:
                f.write(f"mock image data for {size}/test{i}.jpg")
    
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

# Tests for HtmlProcessor
class TestHtmlProcessor:
    def test_process(self, temp_dir, html_test_file, json_test_file):
        # Create processor with dependencies
        json_reader = JsonFileReader()
        html_reader = TextFileReader()
        html_writer = TextFileWriter()
        template_engine = HtmlTemplate()
        processor = HtmlProcessor(json_reader, html_reader, html_writer, template_engine)
        
        # Get test paths
        html_path, _ = html_test_file
        _, json_data = json_test_file
        output_path = os.path.join(temp_dir, "output.html")
        
        # Process the HTML
        result = processor.process(json_data, html_path, output_path)
        
        # Check that output file exists
        assert os.path.exists(output_path)
        
        # Check content
        assert "Test Title" in result
        assert "Test Header" in result
        assert "Test Content" in result
        
        # Check that placeholders are replaced
        assert "{{TITLE}}" not in result
        assert "{{HEADER}}" not in result
        assert "{{CONTENT}}" not in result
    
    def test_process_with_images(self, temp_dir, html_test_file, json_test_file, image_dir, image_placeholders_file, monkeypatch):
        # Set up dependencies
        json_reader = JsonFileReader()
        html_reader = TextFileReader()
        html_writer = TextFileWriter()
        template_engine = HtmlTemplate()
        directory_manager = FileSystemDirectoryManager()
        file_copier = FileSystemCopier()
        image_selector = ImageSelector(directory_manager, file_copier)
        image_processor = ImagePlaceholderProcessor(image_selector, directory_manager)
        
        # Create processor with all dependencies
        processor = HtmlProcessor(
            json_reader, html_reader, html_writer, template_engine, image_processor
        )
        
        # Get test paths
        html_path, _ = html_test_file
        json_path, _ = json_test_file
        img_placeholders_path, _ = image_placeholders_file
        output_path = os.path.join(temp_dir, "output.html")
        dest_img_folder = os.path.join(temp_dir, "assets/img/temp")
        
        # Override JSON data with template-specific data
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "{{TITLE}}": "Test Title",
                "{{HEADER}}": "Test Header",
                "{{CONTENT}}": "Test Content with Images"
            }, f)
        
        # Mock random.choice to make the test deterministic
        monkeypatch.setattr(random, 'choice', lambda x: x[0])
        
        # Process the HTML with images
        result = processor.process_with_images(
            json_path, 
            html_path, 
            output_path,
            img_placeholders_path,
            image_dir,
            dest_img_folder
        )
        
        # Check result
        assert os.path.exists(output_path)
        assert "Test Title" in result
        assert "Test Content with Images" in result
        assert '"assets/img/temp/test0.jpg"' in result
        assert os.path.exists(os.path.join(dest_img_folder, "test0.jpg"))
    
    def test_process_with_images_no_image_processor(self, temp_dir, html_test_file, json_test_file, image_placeholders_file):
        # Set up processor without image processor
        processor = HtmlProcessor(
            JsonFileReader(),
            TextFileReader(),
            TextFileWriter(),
            HtmlTemplate()
            # No image processor
        )
        
        # Get test paths
        html_path, _ = html_test_file
        json_path, _ = json_test_file
        img_placeholders_path, _ = image_placeholders_file
        output_path = os.path.join(temp_dir, "output.html")
        
        # Attempt to process with images should raise ValueError
        with pytest.raises(ValueError):
            processor.process_with_images(
                json_path,
                html_path,
                output_path,
                img_placeholders_path,
                "source",
                "dest"
            )