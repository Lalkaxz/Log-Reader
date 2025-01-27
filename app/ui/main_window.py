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
        
        # Initialize all QActions.
        self.init_actions() 
        
        # Initialize and set Menu bar.
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

        # Initialize and set Tool bar.
        self.toolbar = ToolBar(self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.toolbar)

        self.initUi() 

    # Initialize main UI.
    def initUi(self) -> None:
        self.file_viewer = FileViewer(self) # Initialize text files content viewer.
        self.table_viewer = TableViewer(self) # Initialize database files content viewer.
        self.file_list = FileList(self) # Initialize files display list.
        
        self.splitter = Splitter(self) # Initialize splitter between content viewer and display list.

        self.start_menu = StartMenu(self) # Initialize start menu widget.

        self.central_widget = QStackedWidget() # Initialize stacked widget for change between start menu and file environment.
        self.setCentralWidget(self.central_widget)

        self.central_widget.addWidget(self.start_menu) 
        self.central_widget.addWidget(self.splitter) 


        self.show_start_menu()

        self.setAcceptDrops(True)

    # Initialize QActions.
    def init_actions(self) -> None:
        self.open_file_action = OpenFileAction(self)
        self.open_database_action = OpenDatabaseAction(self)
        self.exit_app_action = ExitAppAction(self)

    # Change current widget to start menu.
    def show_start_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.start_menu)

    # Change current widget to file environment.
    def init_file_env(self) -> None:
        self.central_widget.setCurrentWidget(self.splitter)

    
    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls():
            # Checking dragged file.
            url = e.mimeData().urls()[0] 
            fpath = url.toLocalFile()
            if fpath.endswith((".txt", ".log", ".db", ".sqlite", ".sqlite3", ".db3")): # allowed extensions
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()


    def dropEvent(self, e: QDropEvent) -> None:
        
        # Checking dragged file.
        if not e.mimeData().hasUrls():
            e.ignore()
            return
        
        for url in e.mimeData().urls():
            fpath = url.toLocalFile()

            # If current file is text.
            if fpath.endswith((".txt", ".log")):
                self.open_file_action.handle_open_file(file_path=fpath) # Use open text files handler.
        
            # If current file is database.
            elif fpath.endswith((".db", ".sqlite", ".sqlite3", ".db3")):
                self.open_database_action.handle_open_database(file_path=fpath) # Use open database files handler.
            else:
                e.ignore()