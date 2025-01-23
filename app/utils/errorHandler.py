from PyQt6.QtWidgets import QMessageBox, QWidget


class ErrorHandler:


    @staticmethod
    def show_error_message(content: str, parent: QWidget = None, title: str = "Error") -> None:
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(content)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
