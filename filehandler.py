from abc import ABC, abstractmethod
from typing import Iterator, List, Any
import json
from io import TextIOWrapper, _WrappedBuffer

class FileHandler(ABC):
    # Class variable to track files processed
    _num_files_processed = 0
    _file_cache: dict[str, TextIOWrapper[_WrappedBuffer]] = dict()
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._lines: List[Any] = []
        self._position = 0
    
    def __enter__(self):
        if self.filepath not in FileHandler._file_cache:
            self.file = open(self.filepath, 'r')
            FileHandler._file_cache[self.filepath] = self.file
        else:
            self.file = FileHandler._file_cache[self.filepath]

        self._lines = self.process_file()
        FileHandler._num_files_processed += 1
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
    
    def __iter__(self) -> Iterator[Any]:
        return self
    
    def __next__(self) -> Any:
        if self._position >= len(self._lines):
            raise StopIteration
        item = self._lines[self._position]
        self._position += 1
        return item
    
    @abstractmethod
    def process_file(self) -> List[Any]:
        pass
    
    @classmethod
    def get_files_processed(cls) -> int:
        return cls._num_files_processed
    
    @property
    def current_line_number(self) -> int:
        """
        Returns the current line number being processed.
        """
        return self._position

class TextFileHandler(FileHandler):
    def process_file(self) -> List[str]:
        return [line.strip() for line in self.file]

class CSVFileHandler(FileHandler):
    def process_file(self) -> List[List[str]]:
        return [line.strip().split(',') for line in self.file]

class JSONFileHandler(FileHandler):
    def process_file(self) -> List[dict]:
        return json.load(self.file)

# Example usage
def process_files(files: List[tuple[str, FileHandler]]) -> None:
    for filepath, handler_class in files:
        try:
            with handler_class(filepath) as file_handler:
                print(f"Processing {filepath}:")
                for item in file_handler:
                    print(f"  {item}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")