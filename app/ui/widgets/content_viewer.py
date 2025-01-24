from PyQt6.QtWidgets import  QPlainTextEdit, QTableView, QAbstractItemView, QHeaderView
from PyQt6.QtCore import QTimer, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor, QBrush
from ...utils.fileHandler import FileHandler
from ...utils.databaseHandler import DatabaseHandler
from PyQt6.QtCore import Qt
import pandas as pd
import sqlite3



class FileViewer(QPlainTextEdit):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        self.resize(600, 400)
        self.setReadOnly(True)
        self.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_file_content)


    def display_file_content(self, content: str, file_path: str) -> None:
        if self.timer.isActive:
            self.timer.stop()

        if self.parent.start_menu:
            self.parent.initFileEnv()

        self.setPlainText(content)
        self.file_path = file_path

        if self.isHidden:
            self.show()
            
        if not self.parent.table_viewer.isHidden():
            self.parent.table_viewer.hide()
        
        self.resize(500, self.height())
        self.timer.start(1000)



    def update_file_content(self) -> None:
        file_content = FileHandler.read_file(self.file_path)

        if self.toPlainText() != file_content:
            self.setPlainText(file_content)
            

class TableViewer(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.hide()

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table_content)


    def display_table_content(self, data: pd.DataFrame, conn: sqlite3.Connection, table_name: str) -> None:
        self.conn = conn
        self.table_name = table_name


        if self.timer.isActive:
            self.timer.stop()

        if self.parent.start_menu:
            self.parent.initFileEnv()

        self.setModel(TableModel(data))
        if self.isHidden():
            self.show()

        if not self.parent.file_viewer.isHidden():
            self.parent.file_viewer.hide()

        self.resize(500, self.height())
        self.timer.start(1000)


    def update_table_content(self) -> None:
        table_data = DatabaseHandler.get_database_data(db=self.conn, table=self.table_name)
        
        if not self.model()._data.equals(table_data):
            self.model()._data = table_data
            self.model().layoutChanged.emit()


    def search_in_table(self, search_text: str) -> None:
        search_text = search_text.lower()
        
        for row in range(self.model().rowCount(QModelIndex())):
            row_contains_text = False
            for col in range(self.model().columnCount(QModelIndex())):
                index = self.model().index(row, col)
                item = self.model().data(index, Qt.ItemDataRole.DisplayRole)
                if search_text in str(item).lower():
                    row_contains_text = True
                    break
            self.setRowHidden(row, not row_contains_text)
        
        self.show_search_highlight(search_text) 

    def show_search_highlight(self, search_text: str) -> None:
        search_text = search_text.lower()
        
        for row in range(self.model().rowCount(QModelIndex())):
            for col in range(self.model().columnCount(QModelIndex())):
                index = self.model().index(row, col)
                item = self.model().data(index, Qt.ItemDataRole.DisplayRole)
                if search_text in str(item).lower():
                    self.highlight_cell(index) 
                    break

    def highlight_cell(self, index: QModelIndex) -> None:
        self.model().setData(index, QBrush(QColor(0, 120, 215)), role=Qt.ItemDataRole.BackgroundRole)
        self.model().layoutChanged.emit()  

    def reset_highlight(self) -> None:
        self.model().reset_highlight()

    def reset_row_visibility(self):
        for row in range(self.model().rowCount(QModelIndex())):
            self.setRowHidden(row, False) 
        self.update_table_content()



class TableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data
        self._highlighted_cells = {}

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        elif role == Qt.ItemDataRole.BackgroundRole:

            return self._highlighted_cells.get(index, QBrush()) 

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.BackgroundRole:
            self._highlighted_cells[index] = value 
            self.layoutChanged.emit()  
            return True
        return False

    def reset_highlight(self):
        self._highlighted_cells.clear() 
        self.layoutChanged.emit() 