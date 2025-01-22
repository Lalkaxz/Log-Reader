from PyQt6.QtWidgets import  QPlainTextEdit, QTableView, QAbstractItemView, QHeaderView
from PyQt6.QtCore import QTimer, QAbstractTableModel
from ...utils.fileHandler import FileHandler
from PyQt6.QtCore import Qt
import pandas as pd



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
        if not self.timer.isActive:
            self.timer.stop()

        self.setPlainText(content)
        self.file_path = file_path

        if self.isHidden:
            self.show()
            
        self.parent.table_viewer.hide()
        self.resize(500, self.height())
        self.timer.start(1000)



    def update_file_content(self):
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

        self.setGridStyle(Qt.PenStyle.SolidLine)


    def display_table_content(self, data: pd.DataFrame) -> None:
        self.setModel(TableModel(data))
        if self.isHidden():
            self.show()

        self.parent.file_viewer.hide()
        self.resize(500, self.height())




class TableModel(QAbstractTableModel):
    def __init__(self, data: list[list]):
        super().__init__()
        self._data = data
    
    def data(self, index, role) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index) -> int:
        return self._data.shape[0]

    def columnCount(self, index) -> int:
        return self._data.shape[1]

    def headerData(self, section, orientation, role) -> str:

        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])