from PyQt6.QtWidgets import  QPlainTextEdit 



class FileViewer(QPlainTextEdit):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        self.resize(600, 400)
        self.setReadOnly(True)
        self.hide()


    def display_file_content(self, content: str):
        if self.isHidden:
            self.show()

        self.setPlainText(content)

