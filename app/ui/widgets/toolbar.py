from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolBar

class ToolBar(QToolBar):

    def __init__(self, parent=None, 
                 orientation: Qt.Orientation = Qt.Orientation.Vertical,
                 style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonTextUnderIcon) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setOrientation(orientation)
        self.setToolButtonStyle(style)

        self.addAction(self.parent.open_file_action)
        self.addAction(self.parent.open_database_action)
        self.addAction(self.parent.exit_app_action)
    