import sys
from PyQt6.QtWidgets import QFileDialog
from .errorHandler import ErrorHandler

class FileHandler:
    last_opened_dir = "" 

    # Open file dialog and return file path.
    @staticmethod
    def get_open_file(parent) -> str:
        start_dir = FileHandler.last_opened_dir or "." # If last opened direction is provided, use it for file dialog.

        fpath, _ = QFileDialog.getOpenFileName(parent, "Open file", start_dir, "Text files (*.txt);; Log files(*.log) ")
        if fpath:
            FileHandler.last_opened_dir = fpath.rsplit("/", 1)[0] # Set last opened direction.

        return fpath

    # Get file content from path.
    @staticmethod
    def read_file(parent, file_path: str) -> str | None:
        try:
            with open(file_path, mode='r', encoding="Utf-8") as f:
                return f.read()

        except Exception as e:
            ErrorHandler.show_error_message(f"Failed to read file: {e}", parent=parent)
            return None


