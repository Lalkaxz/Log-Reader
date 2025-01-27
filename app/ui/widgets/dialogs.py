from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
)
from PyQt6.QtGui import QTextDocument, QTextCursor, QCloseEvent
from .content_viewer import FileViewer, TableViewer
from ...utils.errorHandler import ErrorHandler
from PyQt6.QtCore import Qt


class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.text_viewer: FileViewer  = self.parent.file_viewer
        self.table_viewer: TableViewer = self.parent.table_viewer

        self.setWindowTitle("Find")
        self.setFixedSize(400, 125)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Initialize dialog widgets.
        self.label = QLabel("Text:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text")

        self.case_sensitive_checkbox = QCheckBox("Match Case")
        self.wrap_text_checkbox = QCheckBox("Match whole word")

        # Initialize Push Button, call function when clicked.
        self.find_button = QPushButton("Find Next")
        self.find_button.setEnabled(False)
        self.find_button.clicked.connect(self.handle_find)
        
        # Initialize Cancel Push Button, call function when clicked.
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.handle_cancel)

        # Initialize layouts.
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.search_input)

        options_layout = QVBoxLayout()
        options_layout.addWidget(self.case_sensitive_checkbox)
        options_layout.addWidget(self.wrap_text_checkbox)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.find_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(options_layout)
        main_layout.addLayout(buttons_layout)

        final_layout = QVBoxLayout()
        final_layout.addLayout(input_layout)
        final_layout.addLayout(main_layout)

        self.setLayout(final_layout)
        # Call function if input text is changed.
        self.search_input.textChanged.connect(self.toggle_find_button)

    # If input text is not empty, set enabled button.
    def toggle_find_button(self) -> None:
        self.find_button.setEnabled(bool(self.search_input.text()))

    # Handler find action.
    def handle_find(self) -> None:
        search_text = self.search_input.text()
        # Creating flags list. Checking checkbox, add flags to list if checkbox enabled.
        flags = QTextDocument.FindFlag(0)

        if self.case_sensitive_checkbox.isChecked():
            flags |= (QTextDocument.FindFlag.FindCaseSensitively)

        if self.wrap_text_checkbox.isChecked():
            flags |= (QTextDocument.FindFlag.FindWholeWords)

        # If current viewer widget is text viewer.
        if self.parent.splitter.viewer_widget.currentWidget() == self.text_viewer:
            self.text_viewer.search_in_file(search_text, flags)

        # If current viewer widget is database table viewer.
        else:
            self.table_viewer.search_in_table(search_text)
        
    # Handler cancel action.
    def handle_cancel(self) -> None:
        self.close()

    # Handler close event.
    def closeEvent(self, e: QCloseEvent) -> None:
        # If current viewer widget is database table viewer.
        if self.parent.splitter.viewer_widget.currentWidget() == self.table_viewer:
            # Reset highlight and show all table rows.
            self.table_viewer.reset_row_visibility()
            self.table_viewer.reset_highlight()
        e.accept()

