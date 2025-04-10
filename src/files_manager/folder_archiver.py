import io
import os
import zipfile

from src.files_manager.helper.base import FolderArchiver

from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

class ZipFolderArchiver(FolderArchiver):
    """Concrete implementation for zipping folders"""
    def archive(self, folder_path):
        """Zip the contents of folder_path and return the bytes"""
        try:
            # Explicit check for folder existence
            if not os.path.exists(folder_path):
                error_msg = f"Folder not found: {folder_path}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            # Also check if it's actually a directory
            if not os.path.isdir(folder_path):
                error_msg = f"Path exists but is not a directory: {folder_path}"
                logger.error(error_msg)
                raise NotADirectoryError(error_msg)
            
            # Normalize the folder path to handle both relative and absolute paths
            folder_path = os.path.abspath(folder_path)
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Use folder_path directly as the base path for relative calculation
                base_dir = folder_path
                
                # os.walk will not raise FileNotFoundError if folder doesn't exist
                # so we need the explicit check above
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate the relative path for the file in the zip
                        # This will ensure the top folder's name is not included
                        rel_path = os.path.relpath(file_path, base_dir)
                        zipf.write(file_path, rel_path)
            
            zip_buffer.seek(0)
            logger.info(f"Successfully created zip archive for folder: {folder_path}")
            return zip_buffer.getvalue()
        except FileNotFoundError:
            # Re-raise FileNotFoundError directly
            raise
        except Exception as e:
            logger.exception(f"Failed to zip folder: {folder_path}")
            raise