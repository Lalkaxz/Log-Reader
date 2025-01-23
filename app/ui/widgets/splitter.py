from PyQt6.QtWidgets import QSplitter
from PyQt6.QtCore import Qt

class Splitter(QSplitter):

    def __init__(self, parent=None):
        super().__init__(orientation=Qt.Orientation.Horizontal, parent=parent)
        self.parent = parent


        self.addWidget(self.parent.file_list)
        self.addWidget(self.parent.file_viewer)
        self.addWidget(self.parent.table_viewer)

        self.setHandleWidth(3)
        self.setStyleSheet("""
            QSplitter::handle {
                background-color: #CCCCCC; 
                margin-left: 1px;
                margin-right: 1px;
            } """)

