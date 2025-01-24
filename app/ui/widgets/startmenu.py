from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class StartMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.drag_and_drop_widget = DragAndDropWidget(self.parent)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.drag_and_drop_widget)

        self.setLayout(self.main_layout)
       


class DragAndDropWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drag and drop files here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            """
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
                color: #555;
                font-size: 16px;
                padding: 20px;
            }
            """
        )

