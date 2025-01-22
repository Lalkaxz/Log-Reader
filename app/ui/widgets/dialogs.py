from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
)
from PyQt6.QtCore import Qt


class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Найти")
        self.setFixedSize(400, 125)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Widgets
        self.label = QLabel("Что:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска")

        self.case_sensitive_checkbox = QCheckBox("С учетом регистра")
        self.wrap_text_checkbox = QCheckBox("Обтекание текстом")

        self.direction_group = QGroupBox("Направление")
        self.direction_up = QRadioButton("Вверх")
        self.direction_down = QRadioButton("Вниз")
        self.direction_down.setChecked(True)

        direction_layout = QHBoxLayout()
        direction_layout.addWidget(self.direction_up)
        direction_layout.addWidget(self.direction_down)
        self.direction_group.setLayout(direction_layout)

        self.find_button = QPushButton("Найти далее")
        self.find_button.setEnabled(False)
        self.cancel_button = QPushButton("Отмена")

        # Layouts
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
        main_layout.addWidget(self.direction_group)
        main_layout.addLayout(buttons_layout)

        final_layout = QVBoxLayout()
        final_layout.addLayout(input_layout)
        final_layout.addLayout(main_layout)

        self.setLayout(final_layout)

        # Signals
        self.search_input.textChanged.connect(self.toggle_find_button)

        # Stylesheet for matching appearance
        self.setStyleSheet("""
            QDialog {
                background-color: #F0F0F0;
            }
            QLabel, QCheckBox, QRadioButton, QGroupBox {
                font-size: 10pt;
            }
            QLineEdit {
                border: 1px solid #A9A9A9;
                padding: 4px;
            }
            QPushButton {
                min-height: 25px;
                background-color: #E1E1E1;
                border: 1px solid #A9A9A9;
            }
            QPushButton:disabled {
                background-color: #F5F5F5;
                color: #A9A9A9;
                border: 1px solid #D3D3D3;
            }
        """)

    def toggle_find_button(self):
        """Enable/Disable the Find button based on input text."""
        self.find_button.setEnabled(bool(self.search_input.text().strip()))
