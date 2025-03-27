from PyQt6.QtWidgets import  QPlainTextEdit, QTableView, QAbstractItemView, QHeaderView
from PyQt6.QtCore import QTimer, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor, QBrush, QTextDocument, QTextCursor
from ...utils.fileHandler import FileHandler
from ...utils.databaseHandler import DatabaseHandler
from ...utils.errorHandler import ErrorHandler
from PyQt6.QtCore import Qt
import pandas as pd
import sqlite3

COOLDOWN_UPDATE_CONTENT = 1000

# Widget for displaying text file contents.
class FileViewer(QPlainTextEdit):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setReadOnly(True)
        # Timer for auto-update content.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_file_content) # Call function when timeout.

    # Display text on widget.
    def display_file_content(self, content: str, file_path: str) -> None:
        if self.timer.isActive:
            self.timer.stop()
        # Set text on widget and save file path for auto-update.
        self.setPlainText(content)
        self.file_path = file_path
        # Show file viewer widget and start timer.
        self.parent.splitter.show_file_viewer()
        self.timer.start(COOLDOWN_UPDATE_CONTENT)


    # Update text on widget if file is changed.
    def update_file_content(self) -> None:
        # Get current text from file.
        file_content = FileHandler.read_file(self.parent, self.file_path)
        if not file_content:
            return

        if self.toPlainText() != file_content:
            # Save the current scroll positions
            vertical_scroll_bar = self.verticalScrollBar()
            current_vertical_position = vertical_scroll_bar.value()

            # Update the content
            self.setPlainText(file_content)

            # Restore the scroll positions
            vertical_scroll_bar.setValue(current_vertical_position)

    # Search text in widget content.
    def search_in_file(self, search_text: str, flags: QTextDocument.FindFlag) -> None:
        found = self.find(search_text, flags)
        # If input text not found.
        if not found:
            # Move cursor to start of the text.
            self.moveCursor(QTextCursor.MoveOperation.Start)
            # Start search from the start.
            found = self.find(search_text, flags) 
            if not found:
                ErrorHandler.show_info_message(content=f'Text "{search_text}" not found', parent=self.parent)
            

# Widget for displaying database table contents.
class TableViewer(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Configure table headers to adjust size.
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Enable smooth scrolling.
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        # Timer for auto-update content.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table_content)

    # Display table data.
    def display_table_content(self, data: pd.DataFrame, conn: sqlite3.Connection, table_name: str) -> None:
        if self.timer.isActive:
            self.timer.stop()

        self.conn = conn
        self.table_name = table_name

        # Set table model with new data.
        self.setModel(TableModel(data))
        self.model().layoutChanged.emit()
        # Show table viewer widget and start timer.
        self.parent.splitter.show_table_viewer()
        self.timer.start(COOLDOWN_UPDATE_CONTENT)

    # Update data on widget if table is changed.
    def update_table_content(self) -> None:
        table_data = DatabaseHandler.get_database_data(parent=self.parent, db=self.conn, table=self.table_name)
        
        # If table data has changed, update model.
        if not self.model()._data.equals(table_data):
            self.model()._data = table_data
            self.model().layoutChanged.emit()

    # Find text table and hide rows that do not contain need text.
    def search_in_table(self, search_text: str) -> None:
        self.reset_highlight()  # Clear all highlights.
        search_text = search_text.lower()

        any_row_found = False # Flag to track if text found in any rows.

        # Check all table item and compare it with searched text. 
        for row in range(self.model().rowCount(QModelIndex())):
            row_contains_text = False  # Flag to track if text found in current row.

            for col in range(self.model().columnCount(QModelIndex())):
                index = self.model().index(row, col)
                item = self.model().data(index, Qt.ItemDataRole.DisplayRole)
                
                # If text is found, stop searching and change flag.
                if search_text in str(item).lower():
                    row_contains_text = True
                    break  # No need to search further in this row

            self.setRowHidden(row, not row_contains_text)  # Hide row if it doesn't contain the search text.

            # If the current row contains text, change flag.
            if row_contains_text:
                any_row_found = True

        # Show highlight for found text
        self.show_search_highlight(search_text)

        # If the text is not found, reset the visibility rows and show a message.
        if not any_row_found:
            self.reset_row_visibility()
            self.reset_highlight()
            ErrorHandler.show_info_message(content=f'Text "{search_text}" not found', parent=self.parent)

    # Highlight cell that do contain need text.
    def show_search_highlight(self, search_text: str) -> None:
        search_text = search_text.lower()
        
        # If text is found, highlight this cell.
        for row in range(self.model().rowCount(QModelIndex())):
            for col in range(self.model().columnCount(QModelIndex())):
                index = self.model().index(row, col)
                item = self.model().data(index, Qt.ItemDataRole.DisplayRole)
                if search_text in str(item).lower():
                    self.highlight_cell(index) 


    # Highlight cell with required index.
    def highlight_cell(self, index: QModelIndex) -> None:
        self.model().setData(index, QBrush(QColor(0, 120, 215)), role=Qt.ItemDataRole.BackgroundRole)
        self.model().layoutChanged.emit()  

    # Clear all highlight.
    def reset_highlight(self) -> None:
        self.model().reset_highlight()

    # Show all table rows.
    def reset_row_visibility(self) -> None:
        for row in range(self.model().rowCount(QModelIndex())):
            self.setRowHidden(row, False) 
        self.update_table_content()


# Custom table model for handling and displaying pandas DataFrame data.
class TableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data 
        self._highlighted_cells = {}  # Dict to track highlighted cells.

    # Get data for a specific cell based on the role.
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # Return the cell value as a string for display.
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        elif role == Qt.ItemDataRole.BackgroundRole:
            # Return the highlight color for the cell if it exists.
            return self._highlighted_cells.get(index, QBrush())

    # Return the number of rows in the DataFrame.
    def rowCount(self, index) -> tuple[int, int]:
        return self._data.shape[0]

    # Return the number of columns in the DataFrame.
    def columnCount(self, index) -> tuple[int, int]:
        return self._data.shape[1]

    # Provide header data for table columns and rows.
    def headerData(self, section, orientation, role) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])  # Column headers.
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])  # Row headers.

    # Set data for a specific cell, typically for background highlights.
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.BackgroundRole:
            self._highlighted_cells[index] = value  # Add or update highlight for the cell.
            self.layoutChanged.emit()
            return True
        return False

    # Clear all highlights in the table.
    def reset_highlight(self) -> None:
        self._highlighted_cells.clear()
        self.layoutChanged.emit()