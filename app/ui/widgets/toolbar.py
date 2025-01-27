from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolBar

class ToolBar(QToolBar):

    def __init__(self, parent=None, 
                 orientation: Qt.Orientation = Qt.Orientation.Vertical) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setOrientation(orientation)

        # Add actions in toolbar.
        self.addAction(self.parent.open_file_action)
        self.addAction(self.parent.open_database_action)
        self.addAction(self.parent.exit_app_action)
    