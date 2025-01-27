from PyQt6.QtWidgets import QSplitter, QStackedWidget
from PyQt6.QtCore import Qt

class Splitter(QSplitter):

    def __init__(self, parent=None):
        super().__init__(orientation=Qt.Orientation.Horizontal, parent=parent)
        self.parent = parent

        # Init stacked widget to change between file and database tables content viewer.
        self.viewer_widget = QStackedWidget() 
        self.viewer_widget.addWidget(self.parent.file_viewer)
        self.viewer_widget.addWidget(self.parent.table_viewer)

        self.addWidget(self.parent.file_list)
        self.addWidget(self.viewer_widget)

        self.setHandleWidth(3)
        self.setStyleSheet("""
            QSplitter::handle {
                background-color: #CCCCCC; 
                margin-left: 1px;
                margin-right: 1px;
            } """)
        
    # Set current widget to file content viewer.
    def show_file_viewer(self) -> None:
        self.viewer_widget.setCurrentWidget(self.parent.file_viewer)

    # Set current widget to database tables content viewer.
    def show_table_viewer(self) -> None:
        self.viewer_widget.setCurrentWidget(self.parent.table_viewer)

