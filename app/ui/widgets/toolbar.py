from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QToolBar, QWidget, QSizePolicy

class ToolBar(QToolBar):

    def __init__(self, parent, 
                 orientation: Qt.Orientation = Qt.Orientation.Horizontal,
                 style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonTextUnderIcon) -> None:
        super().__init__(parent)
        self.setOrientation(orientation)
        self.setToolButtonStyle(style)