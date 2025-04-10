import pytest
import os
import io
import zipfile
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from src.files_manager.folder_archiver import ZipFolderArchiver

# Import the classes to test


@pytest.fixture
def temp_folder():
    """Create a temporary folder structure for testing"""
    temp_dir = tempfile.mkdtemp()

    # Create a nested directory structure
    subdir1 = os.path.join(temp_dir, "subdir1")
    subdir2 = os.path.join(temp_dir, "subdir2")
    nested_dir = os.path.join(subdir1, "nested")

    os.makedirs(subdir1)
    os.makedirs(subdir2)
    os.makedirs(nested_dir)

    # Create some test files
    test_files = [
        os.path.join(temp_dir, "root_file.txt"),
        os.path.join(subdir1, "file1.txt"),
        os.path.join(subdir2, "file2.txt"),
        os.path.join(nested_dir, "nested_file.txt"),
    ]

    # Write content to the test files
    for i, file_path in enumerate(test_files):
        with open(file_path, "w") as f:
            f.write(f"Test content {i}")

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


class TestZipFolderArchiver:
    def test_archive_creates_valid_zip(self, temp_folder):
        """Test that archive creates a valid zip file with correct structure"""
        # Create the archiver
        archiver = ZipFolderArchiver()

        # Archive the folder
        zip_data = archiver.archive(temp_folder)

        # Verify that zip_data is bytes
        assert isinstance(zip_data, bytes)

        # Create a file-like object from the bytes
        zip_buffer = io.BytesIO(zip_data)

        # Check that it's a valid zip file
        assert zipfile.is_zipfile(zip_buffer)

        # Open the zip file and check its contents
        with zipfile.ZipFile(zip_buffer) as zipf:
            # Check that the zip file is valid
            assert zipf.testzip() is None

            # Check that all expected files are in the zip
            file_list = zipf.namelist()
            
            temp_folder_name = os.path.basename(os.path.dirname(f"{temp_folder}/"))

            # With the fix, files are stored directly at root level
            assert f"root_file.txt" in file_list
            assert f"subdir1/file1.txt" in file_list
            assert f"subdir2/file2.txt" in file_list
            assert f"subdir1/nested/nested_file.txt" in file_list

            # Verify content of a file
            with zipf.open(f"root_file.txt") as f:
                content = f.read().decode("utf-8")
                assert content == "Test content 0"

    def test_archive_empty_folder(self):
        """Test archiving an empty folder"""
        # Create an empty temporary directory
        temp_dir = tempfile.mkdtemp()

        try:
            archiver = ZipFolderArchiver()
            zip_data = archiver.archive(temp_dir)

            # Verify that zip_data is bytes
            assert isinstance(zip_data, bytes)

            # Create a file-like object from the bytes
            zip_buffer = io.BytesIO(zip_data)

            # Check that it's a valid zip file, though empty
            assert zipfile.is_zipfile(zip_buffer)

            with zipfile.ZipFile(zip_buffer) as zipf:
                # An empty directory might not have any entries in the zip file
                assert len(zipf.namelist()) == 0
        finally:
            # Cleanup
            shutil.rmtree(temp_dir)

    def test_archive_nonexistent_folder(self):
        """Test that archiving a nonexistent folder raises FileNotFoundError"""
        archiver = ZipFolderArchiver()

        with pytest.raises(FileNotFoundError):
            archiver.archive("/path/to/nonexistent/folder")
