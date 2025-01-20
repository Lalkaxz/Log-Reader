from PyQt6.QtWidgets import  QPlainTextEdit 
from PyQt6.QtCore import QTimer
from ...utils.fileHandler import FileHandler



class FileViewer(QPlainTextEdit):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        self.resize(600, 400)
        self.setReadOnly(True)
        self.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_file_content)


    def display_file_content(self, content: str, file_path: str) -> None:
        if not self.timer.isActive:
            self.timer.stop()

        self.setPlainText(content)
        self.file_path = file_path

        if self.isHidden:
            self.show()

        self.timer.start(1000)



    def update_file_content(self):
        file_content = FileHandler.read_file(self.file_path)

        if self.toPlainText() != file_content:
            self.setPlainText(file_content)
            


