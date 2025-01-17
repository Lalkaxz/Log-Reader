from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import *
from ..actions.action import OpenFileAction, ConnectDatabaseAction

class MenuBar(QMenuBar):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.file_menu = self.addMenu("File")
        

        self.file_menu.addAction(OpenFileAction(self))
        self.file_menu.addAction(ConnectDatabaseAction(self))

