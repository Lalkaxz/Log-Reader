from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction, QKeySequence
from .dialogs import FindDialog

class MenuBar(QMenuBar):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent

        self.file_menu = self.addMenu("File")

        self.file_menu.addAction(self.parent.open_file_action)
        self.file_menu.addAction(self.parent.open_database_action)
        self.file_menu.addAction(self.parent.exit_app_action)

        self.edit_menu = self.addMenu("Edit")

        self.copy_action = QAction("Copy", self, shortcut=QKeySequence.StandardKey.Copy, triggered=self.handle_copy)
        self.edit_menu.addAction(self.copy_action)

        self.find_action = QAction("Find", self, shortcut="Ctrl+F", triggered=self.handle_find)
        self.edit_menu.addAction(self.find_action)

        self.select_all_action = QAction("Select All", self, shortcut=QKeySequence.StandardKey.SelectAll, triggered=self.handle_select_all)
        self.edit_menu.addAction(self.select_all_action)
    

    def handle_copy(self):
        plainText = self.parent.file_viewer
        plainText.copy()


    def handle_find(self):
        find_dialog = FindDialog(self.parent)
        find_dialog.exec()


    def handle_select_all(self):
        plainText = self.parent.file_viewer
        plainText.selectAll()

