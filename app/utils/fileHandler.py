import sys
from PyQt6.QtWidgets import QFileDialog


class FileHandler:
    last_opened_dir = ""

    @staticmethod
    def get_open_file(parent) -> str:
        start_dir = FileHandler.last_opened_dir or "."

        fpath, _ = QFileDialog.getOpenFileName(parent, "Open file", start_dir, "Text files (*.txt);; Log files(*.log) ")
        if fpath:
            FileHandler.last_opened_dir = fpath.rsplit("/", 1)[0]

        return fpath


    @staticmethod
    def read_file(file_path: str) -> str:
        try:
            with open(file_path, mode='r', encoding="Utf-8") as f:
                return f.read()

        except Exception as e:
            print(f"Failed to read file: {e}")

