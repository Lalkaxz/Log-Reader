import sys
from PyQt6.QtWidgets import QFileDialog

class FileHandler:
    
    @staticmethod
    def get_open_file(parent) -> str:
        fpath, _ = QFileDialog.getOpenFileName(parent, "Open file", ".", "Text files (*.txt);; Log files(*.log) ")
        return fpath


    @staticmethod
    def read_file(file_path: str) -> str:
        try:
            with open(file_path, mode='r', encoding="Utf-8") as f:
                return f.read()

        except Exception as e:
            print(f"Failed to read file: {e}")

