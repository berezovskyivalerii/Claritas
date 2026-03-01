from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PySide6.QtCore import QFile, QLine, Qt, Signal
from config.config import BarConfig

class BarSettingsWidget(QWidget):
    request_chart_draw = Signal(str, object)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Chart Title...")

        # Inputs specific to Line Charts
        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("X Axis Label...")
        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("Y Axis Label...")
        
        layout.addWidget(QLabel("Bar Chart Settings"))
        layout.addWidget(self.x_input)
        layout.addWidget(self.y_input)

    def create_config(self, path, raw_x, raw_y) -> BarConfig:
        config = BarConfig(
            path=path,
            title=self.title_input.text(),
            categories=raw_x,
            values=raw_y,
            x_label=self.x_input.text(),
            y_label=self.y_input.text()
        )
        
        return config
