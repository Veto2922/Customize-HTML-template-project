from abc import ABC, abstractmethod

class FileReader(ABC):
    """Abstract interface for file reading operations"""
    @abstractmethod
    def read(self, path):
        pass

class FileWriter(ABC):
    """Abstract interface for file writing operations"""
    @abstractmethod
    def write(self, content, path):
        pass

class FileCopier(ABC):
    """Abstract interface for file copying operations"""
    @abstractmethod
    def copy(self, source_path, destination_path):
        pass

class DirectoryManager(ABC):
    """Abstract interface for directory operations"""
    @abstractmethod
    def ensure_directory_exists(self, directory_path):
        pass
    
    @abstractmethod
    def list_files_with_extensions(self, directory_path, extensions):
        pass