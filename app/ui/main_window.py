from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from .widgets.menubar import MenuBar
from .widgets.displaylist import FileList
from .widgets.content_viewer import FileViewer

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
        self.file_list = FileList(self)
        
        
        self.splitter = QSplitter(orientation=Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.file_list)
        self.splitter.addWidget(self.file_viewer)

        self.splitter.setHandleWidth(3)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #CCCCCC; 
                margin-left: 2px;
                margin-right: 2px;
            }
        """)
        self.setCentralWidget(self.splitter)

    
        