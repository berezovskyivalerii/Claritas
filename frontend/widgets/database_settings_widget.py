import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QDialog,
    QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox
)

class DatabaseSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(300)

        # Create layout
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # Input fields
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("localhost")
        
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.db_name_input = QLineEdit()

        # Add fields to form
        self.form_layout.addRow("Host:", self.host_input)
        self.form_layout.addRow("User:", self.user_input)
        self.form_layout.addRow("Password:", self.password_input)
        self.form_layout.addRow("Database:", self.db_name_input)

        self.layout.addLayout(self.form_layout)

        # Standard dialog buttons (OK and Cancel)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_data(self):
        """Returns the entered data as a dictionary."""
        return {
            "host": self.host_input.text(),
            "user": self.user_input.text(),
            "password": self.password_input.text(),
            "database": self.db_name_input.text()
        }
