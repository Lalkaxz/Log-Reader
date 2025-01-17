from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from .widgets.menubar import MenuBar


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Log Reader")

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

        self.plainText = QPlainTextEdit(self)
        self.setCentralWidget(self.plainText)