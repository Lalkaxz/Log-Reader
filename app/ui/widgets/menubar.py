from PyQt6.QtWidgets import QMenuBar, QApplication, QStyleFactory
from PyQt6.QtGui import QAction, QKeySequence
from .dialogs import FindDialog

class MenuBar(QMenuBar):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent

        self.file_menu = self.addMenu("File")

        # Add actions in toolbar.
        self.file_menu.addAction(self.parent.open_file_action)
        self.file_menu.addAction(self.parent.open_database_action)
        self.file_menu.addAction(self.parent.exit_app_action)
        
        self.edit_menu = self.addMenu("Edit")

        # Copy action in text file editor.
        self.copy_action = QAction("Copy", self, 
                                   shortcut=QKeySequence.StandardKey.Copy,
                                   triggered=self.handle_copy)
        self.edit_menu.addAction(self.copy_action)

        # Find action for open find dialog.
        self.find_action = QAction("Find", self, 
                                   shortcut="Ctrl+F", 
                                   triggered=self.handle_find)
        self.edit_menu.addAction(self.find_action)

        # Selection action for select all text in file editor.
        self.select_all_action = QAction("Select All", self, 
                                         shortcut=QKeySequence.StandardKey.SelectAll, 
                                         triggered=self.handle_select_all)
        self.edit_menu.addAction(self.select_all_action)

        self.view_menu = self.addMenu("View")

        # Toolbar action for hide/show toolbar in application.
        self.toolbar_action = QAction("Toggle Toolbar", self, triggered=self.handle_toggle_toolbar)
        self.view_menu.addAction(self.toolbar_action)

        # Style menu for change application styles.
        self.style_menu = self.view_menu.addMenu("Style")
        self.handle_init_styles()

    # Set avaible styles in change style menu.
    def handle_init_styles(self) -> None:
        available_styles = QStyleFactory.keys()
        for style_name in available_styles:
            style_action = QAction(style_name, self)
            style_action.triggered.connect(self.set_application_style)
            self.style_menu.addAction(style_action)

    # Change current application style.
    def set_application_style(self) -> None:
        QApplication.setStyle(self.sender().text()) # Get triggered style from function sender.


    # Copy text from file viewer.
    def handle_copy(self) -> None:
        plainText = self.parent.file_viewer
        plainText.copy()

    # Open find dialog.
    def handle_find(self) -> None:
        find_dialog = FindDialog(self.parent)
        find_dialog.exec()

    # Select all text from file viewer.
    def handle_select_all(self) -> None:
        plainText = self.parent.file_viewer
        plainText.selectAll()

    # Toggle visibility of toolbar.
    def handle_toggle_toolbar(self) -> None:
        if self.parent.toolbar.isHidden():
            self.parent.toolbar.show()
        else:
            self.parent.toolbar.hide()