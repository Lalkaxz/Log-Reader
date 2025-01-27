from PyQt6.QtWidgets import QMessageBox, QWidget


class ErrorHandler:

    # Show error message dialog.
    @staticmethod
    def show_error_message(content: str, parent: QWidget = None, title: str = "Error") -> None:
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(content)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    # Show info message dialog.
    @staticmethod
    def show_info_message(content: str, parent: QWidget = None, title: str = "Info") -> None:
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(content)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()