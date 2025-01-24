from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QDropEvent, QDragEnterEvent
from .widgets.menubar import MenuBar
from .widgets.displaylist import FileList
from .widgets.content_viewer import FileViewer, TableViewer
from .widgets.splitter import Splitter
from .actions.action import OpenFileAction, OpenDatabaseAction, ExitAppAction
from .widgets.startmenu import StartMenu
from .widgets.toolbar import ToolBar
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Log Reader")
        self.resize(700, 600)

        self.initActions() 

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

        self.toolbar = ToolBar(self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.toolbar)

        self.initUi() 

    # initialize main UI
    def initUi(self) -> None:
        self.file_viewer = FileViewer(self) # init text files content viewer
        self.table_viewer = TableViewer(self) # init database files content viewer
        self.file_list = FileList(self) # init files display list
        
        
        self.splitter = Splitter(self) # init splitter between content viewer and display list
        self.splitter.hide()

        self.start_menu = StartMenu(self) # init start menu widget

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.addWidget(self.start_menu) 
        self.central_widget.addWidget(self.splitter) 


        self.showStartMenu()

        self.setAcceptDrops(True)

    # initialize QActions
    def initActions(self) -> None:
        self.open_file_action = OpenFileAction(self)
        self.open_database_action = OpenDatabaseAction(self)
        self.exit_app_action = ExitAppAction(self)

    
    def showStartMenu(self) -> None:
        self.central_widget.setCurrentWidget(self.start_menu)

    # change current widget to file environment
    def initFileEnv(self) -> None:
        self.central_widget.setCurrentWidget(self.splitter)

    
    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls():
            # checking dragged file 
            url = e.mimeData().urls()[0] 
            fpath = url.toLocalFile()
            if fpath.endswith((".txt", ".log", ".db", ".sqlite", ".sqlite3", ".db3")):
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()


    def dropEvent(self, e: QDropEvent) -> None:
        
        # checking dragged file 
        if not e.mimeData().hasUrls():
            e.ignore()
            return
        
        for url in e.mimeData().urls():
            fpath = url.toLocalFile()

            # if current file is text
            if fpath.endswith((".txt", ".log")):
                self.open_file_action.handle_open_file(file_path=fpath) # use open text files handler
        
            # if current file is database
            elif fpath.endswith((".db", ".sqlite", ".sqlite3", ".db3")):
                self.open_database_action.handle_open_database(file_path=fpath) # use open database files handler
                self.initFileEnv() # change current widget to file enviroment
            else:
                e.ignore()