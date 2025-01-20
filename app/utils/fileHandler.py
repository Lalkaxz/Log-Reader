import sys
import sqlite3
from PyQt6.QtWidgets import QFileDialog

class FileHandler:
    
    @staticmethod
    def open_file(parent) -> str:
        fname, _ = QFileDialog.getOpenFileName(parent, "Open file", ".", "Text files (*.txt);; Log files(*.log) ")
        return fname


    @staticmethod
    def read_file(file_path: str) -> str:
        try:
            with open(file_path, mode='r', encoding="Utf-8") as f:
                return f.read()

        except Exception as e:
            raise IOError(f"Failed to read file: {e}")

