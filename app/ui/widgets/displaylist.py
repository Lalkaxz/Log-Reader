import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ...utils.fileHandler import FileHandler
from ...utils.databaseHandler import DatabaseHandler


class FileList(QListWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent

        self.setMinimumSize(QSize(100, 400))
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.itemClicked.connect(self.display_content)
        


    def display_content(self, item: QListWidgetItem) -> None:

        item_type = item.data(Qt.ItemDataRole.UserRole + 1)

        if item_type == "file":
            item_path = item.data(Qt.ItemDataRole.UserRole)
            file_content = FileHandler.read_file(item_path)
            self.parent.file_viewer.display_file_content(file_content, item_path)

        else:
            item_path = item.data(Qt.ItemDataRole.UserRole)
            item_connect = DatabaseHandler.connect_database(item_path)
            table_content = DatabaseHandler.get_database_data(item_connect, item.text())
            self.parent.table_viewer.display_table_content(data=table_content, conn=item_connect, table_name=item.text())


    def add_file_to_list(self, file_path: str) -> None:
        type = "file"

        item_name = os.path.basename(file_path)
        item = QListWidgetItem(item_name)
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        item.setData(Qt.ItemDataRole.UserRole + 1, type)

        for existing_item in self.findItems(item.text(), Qt.MatchFlag.MatchExactly):
            if item.text() == existing_item.text():
                return
        
        self.addItem(item)
        self.setCurrentItem(item)

    
    def add_tables_to_list(self, tables: list[str], file_path: str) -> None:
        type = "table"

        for table in tables:
            item = QListWidgetItem(table)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            item.setData(Qt.ItemDataRole.UserRole + 1, type)

            for existing_item in self.findItems(item.text(), Qt.MatchFlag.MatchExactly):
                if item.text() == existing_item.text():
                    break
            else:
                self.addItem(item)

