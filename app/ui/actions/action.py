from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ...utils.fileHandler import FileHandler


class OpenFileAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Open file", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+O")
        self.triggered.connect(self.handle_open_file)


    def handle_open_file(self):
        file_path = FileHandler.open_file(self.parent)
        file_content = FileHandler.read_file(file_path)
        self.parent.file_viewer.display_file_content(file_content, file_path)
        self.parent.file_list.add_file_to_list(file_path)
    


class ConnectDatabaseAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Connect database", parent=parent)
        self.setShortcut("Ctrl+D")


    def connect_database(self) -> None:
        return



class ExitAppAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Exit", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+Q")
        self.triggered.connect(QApplication.exit)



        
