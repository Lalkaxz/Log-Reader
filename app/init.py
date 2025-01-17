from PyQt6.QtWidgets import QApplication
from .ui.main_window import MainWindow
import sys

def run():
    
    app: QApplication = QApplication(sys.argv)

    window: MainWindow = MainWindow()
    window.show()

    return sys.exit(app.exec())