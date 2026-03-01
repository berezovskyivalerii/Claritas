from PySide6.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PySide6.QtCore import QFile, QLine, Qt, Signal
from config.config import LineConfig

class LineSettingsWidget(QWidget):
    request_chart_draw = Signal(str, object)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Chart Title...")

        # Inputs specific to Line Charts
        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("X Axis Label...")
        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("Y Axis Label...")

        # Color
        self.color_input = QComboBox()
        self.color_input.addItems(['Red', 'Blue', "Green", "Black", "Yellow"])

        # Grid
        self.is_grid = QCheckBox("Grid")
        
        layout.addWidget(self.title_input)
        layout.addWidget(self.x_input)
        layout.addWidget(self.y_input)
        layout.addWidget(self.color_input)
        layout.addWidget(self.is_grid)

        self.apply_styles()

    def create_config(self, path, raw_x, raw_y) -> LineConfig:
        config = LineConfig(
            path=path,
            title=self.title_input.text(),
            x_data=raw_x,
            y_data=raw_y,
            x_label=self.x_input.text(),
            y_label=self.y_input.text(),
            color=self.color_input.currentText(),
            is_grid=self.is_grid.isChecked()
        )
        
        return config

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel {
                color: black;
            }

            QCheckBox {
                color: black;
                font-size: 14px;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid black;
                background-color: transparent;
                border-radius: 5px;
            }

            QCheckBox::indicator:checked {
                image: url(black_check_mark.png);
            }
        """)

