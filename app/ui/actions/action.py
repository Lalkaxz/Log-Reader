from PyQt6.QtGui import *


class OpenFileAction(QAction):
    def __init__(self, parent=None):
        super().__init__(text="Open file", parent=parent)
        self.setShortcut("Ctrl+O")


    def open_file(self) -> None:
        return


class ConnectDatabaseAction(QAction):
    def __init__(self, parent=None):
        super().__init__(text="Connect database", parent=parent)
        self.setShortcut("Ctrl+D")


    def connect_database(self) -> None:
        return



        
