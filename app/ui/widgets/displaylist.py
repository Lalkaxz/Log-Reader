import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ...utils.fileHandler import FileHandler


class FileList(QListWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent

        self.resize(100, 400)
        self.setMinimumSize(QSize(100, 400))
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.itemClicked.connect(self.display_content)


    def display_content(self, item) -> None:
        item_path = item.data(Qt.ItemDataRole.UserRole)
        file_content = FileHandler.read_file(item_path)
        self.parent.file_viewer.display_file_content(file_content, item_path)


    def add_file_to_list(self, file_path) -> None:
        item_name = os.path.basename(file_path)
        item = QListWidgetItem(item_name)
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        self.addItem(item)


