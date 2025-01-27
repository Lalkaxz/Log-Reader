import os.path
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QFrame, QListWidget, QListWidgetItem, QStyledItemDelegate
from ...utils.fileHandler import FileHandler
from ...utils.databaseHandler import DatabaseHandler


class FileListDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index) -> None:
        super().paint(painter, option, index)
        # Retrieve the item type from UserRole + 1
        item_type = index.data(Qt.ItemDataRole.UserRole + 1)

        if item_type:
            # Configure the painter for semi-transparent text
            painter.save()
            painter.setPen(QColor(150, 150, 150, 250))  # Gray color with transparency
            rect = option.rect

            # Draw the type text on the right side
            painter.drawText(
                rect.adjusted(-10, 0, -10, 0), 
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                item_type.capitalize(),
            )
            painter.restore()

# List for display all opened files and tables.
class FileList(QListWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent

        self.setMinimumSize(QSize(100, 400))
        self.setFrameShape(QFrame.Shape.StyledPanel)
        # Call functions when a list item has been clicked or activated.
        self.itemClicked.connect(self.handle_display_content)
        self.itemActivated.connect(self.handle_display_content)
        # Set custom delegate for item styling.
        self.setItemDelegate(FileListDelegate())
        
    # Handle clicked item.
    def handle_display_content(self, item: QListWidgetItem) -> None:

        item_type = item.data(Qt.ItemDataRole.UserRole + 1)

        # If item is text file.
        if item_type == "file":
            # Get file path and its contents. Then display this content.
            item_path = item.data(Qt.ItemDataRole.UserRole)
            file_content = FileHandler.read_file(self.parent, item_path)
            if file_content == None:
                return
            self.parent.file_viewer.display_file_content(file_content, item_path)

        # If item is database table.
        else:
            # Get database path, connect to it, then get table content and display its.
            item_path = item.data(Qt.ItemDataRole.UserRole)
            item_connect = DatabaseHandler.connect_database(item_path)
            if item_connect == None:
                return
            table_content = DatabaseHandler.get_database_data(item_connect, item.text())
            if table_content == None:
                return
            self.parent.table_viewer.display_table_content(data=table_content, conn=item_connect, table_name=item.text())

    # Add opened file to list.
    def add_file_to_list(self, file_path: str) -> None:
        type = "file"
        # Get item name from path.
        item_name = os.path.basename(file_path)
        # Creating item and set data to it.
        item = QListWidgetItem(item_name)
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        item.setData(Qt.ItemDataRole.UserRole + 1, type)
        
        if self.check_item_already_exists(item):
            return
        
        # Add item to list and set selection on this item.
        self.addItem(item)
        self.setCurrentItem(item)

    # Add database tables to list.
    def add_tables_to_list(self, tables: list[str], file_path: str) -> None:
        type = "table"

        # Creating items from all tables and add its to list.
        for table in tables:
            item = QListWidgetItem(table)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            item.setData(Qt.ItemDataRole.UserRole + 1, type)

            if self.check_item_already_exists(item):
                return

            self.addItem(item)

    # Checking item already exists in display list.
    def check_item_already_exists(self, item) -> bool:
        for existing_item in self.findItems(item.text(), Qt.MatchFlag.MatchExactly):
            if item.text() == existing_item.text():
                return True
        
        return False

