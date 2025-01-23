from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QDropEvent, QDragEnterEvent
from .widgets.menubar import MenuBar
from .widgets.displaylist import FileList
from .widgets.content_viewer import FileViewer, TableViewer
from .widgets.splitter import Splitter
from .actions.action import OpenFileAction, OpenDatabaseAction


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
        self.file_list = FileList(self)
        
        
        self.splitter = Splitter(self)

        self.setCentralWidget(self.splitter)

        self.setAcceptDrops(True)


    
    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()


    def dropEvent(self, e: QDropEvent) -> None:
        fileClassAction: OpenFileAction = self.menuBar().file_menu.actions()[0]
        databaseClassAction: OpenDatabaseAction = self.menuBar().file_menu.actions()[1]


        if not e.mimeData().hasUrls():
            e.ignore()
            return
        
        for url in e.mimeData().urls():
            fpath = url.toLocalFile()

            if fpath.endswith((".txt", ".log")):
                fileClassAction.handle_open_file(file_path=fpath)
        
            elif fpath.endswith((".db", ".sqlite", ".sqlite3", ".db3")):
                databaseClassAction.handle_open_database(file_path=fpath)

            else:
                e.ignore()

        

        



    
        