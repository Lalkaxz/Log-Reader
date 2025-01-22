from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from .widgets.menubar import MenuBar
from .widgets.displaylist import FileList
from .widgets.content_viewer import FileViewer, TableViewer, TableModel
import pandas as pd

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Log Reader")
        self.resize(QSize(700, 600))

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

        self.initUi()

    def initUi(self) -> None:
        self.file_viewer = FileViewer(self)
        self.table_viewer = TableViewer(self)
        # self.table_viewer.setModel(TableModel(pd.DataFrame([
        #   [1, 9, 2],
        #   [1, 0, -1],
        #   [3, 5, 2],
        #   [3, 3, 2],
        #   [5, 8, 9],
        # ], columns = ['A', 'B', 'C'])))

        self.file_list = FileList(self)
        
        
        self.splitter = QSplitter(orientation=Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.file_list)
        self.splitter.addWidget(self.file_viewer)
        self.splitter.addWidget(self.table_viewer)

        self.splitter.setHandleWidth(3)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #CCCCCC; 
                margin-left: 1px;
                margin-right: 1px;
            }
        """)
        self.setCentralWidget(self.splitter)

    
        