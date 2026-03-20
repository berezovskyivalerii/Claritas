from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

class GreetingWindow(QWidget):
    db_chosen = Signal()
    fs_chosen = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(15)

        self.greeting_text = QLabel("Hello!\nMake your choice!")
        self.greeting_text.setAlignment(Qt.AlignCenter)
        self.greeting_text.setStyleSheet("""
            color: #212121;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        """)

        self.fs_button = QPushButton("File System")
        self.db_button = QPushButton("Database Connection")

        button_style = """
            QPushButton {
                background-color: #2563EB; 
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E3A8A;
            }
        """
        self.fs_button.setStyleSheet(button_style)
        self.db_button.setStyleSheet(button_style)

        self.main_layout.addWidget(self.greeting_text)
        self.main_layout.addWidget(self.fs_button)
        self.main_layout.addWidget(self.db_button)
        
        self.fs_button.clicked.connect(self.fs_chosen.emit)
        self.db_button.clicked.connect(self.db_chosen.emit)

