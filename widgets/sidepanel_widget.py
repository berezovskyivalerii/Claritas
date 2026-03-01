from PySide6.QtWidgets import QStackedWidget, QWidget, QPushButton, QVBoxLayout, QFileDialog, QComboBox
from PySide6.QtCore import Qt, Signal
import pandas
from config.config import BaseConfig, LineConfig
from widgets.bar_settings_widget import BarSettingsWidget
from widgets.line_settings_widget import LineSettingsWidget

class SidePanel(QWidget):
    request_chart_draw = Signal(str, object)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) 

        self.raw_x = []
        self.raw_y = []
        self.chart_type = "Line Chart"
        self.selected_path = ""

        # --- Create Main Layout --- 
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.upload_button = QPushButton("Upload Data File")
        self.upload_button.clicked.connect(self.select_file)

        # Create the ComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItem("Line Chart")
        self.combo_box.addItem("Bar Chart")

        # Create the Stacked Widget
        self.stacked_widget = QStackedWidget()

        self.line_settings = LineSettingsWidget()
        self.bar_settings = BarSettingsWidget()

        self.stacked_widget.addWidget(self.line_settings)
        self.stacked_widget.addWidget(self.bar_settings)

        self.combo_box.currentIndexChanged.connect(self.stacked_widget.setCurrentIndex)
        self.combo_box.currentTextChanged.connect(self.handle_chart_selection)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.get_user_data)

        # Add everything to the main layout
        self.main_layout.addWidget(self.upload_button)
        self.main_layout.addWidget(self.combo_box)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)

        # --- Styles ---
        self.apply_styles()
    
    def get_config(self):
        if not self.selected_path:
            print("Error: no data to save.")
            return None

        active_widget = self.stacked_widget.currentWidget()
        generated_config = active_widget.create_config(self.selected_path, self.raw_x, self.raw_y)

        generated_config.chart_type = self.chart_type.lower()

        return generated_config
    
    def handle_chart_selection(self, chart_type):
        self.chart_type = chart_type

        active_widget = self.stacked_widget.currentWidget()
        generated_config = active_widget.create_config(self.selected_path, self.raw_x, self.raw_y)
        self.request_chart_draw.emit(self.chart_type, generated_config)

    # Read inputs
    def get_user_data(self):
        if not self.raw_y or not self.raw_y:
            print("Error: no data loaded")

        active_widget = self.stacked_widget.currentWidget()

        genereted_config = active_widget.create_config(self.selected_path, self.raw_x, self.raw_y)

        self.request_chart_draw.emit(self.chart_type, genereted_config)

    # Select .csv file
    def select_file(self):
        dialog_filter = "CSV filter (*.csv);;All files (*.*)"

        self.selected_path, _ = QFileDialog.getOpenFileName(None, "Select Data File", "", dialog_filter)
        if self.selected_path: 
            self.parse_selected_file(self.selected_path)

    # Parse file to config
    def parse_selected_file(self, path):
        # read only first and second column
        data_df = pandas.read_csv(path, usecols=[0,1])
        self.raw_x = data_df.iloc[:, 0].tolist()
        self.raw_y = data_df.iloc[:, 1].tolist()
        # TODO: Check if amount of values is the same

    def apply_styles(self):
        self.setStyleSheet("""
            SidePanel {
                background-color: #F5F7FA;
            }

            QComboBox {
                color: black;
            }
            
            QPushButton {
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 12px;
            }
            
            QPushButton:hover {
                background-color: #E6E9ED;
            }
            
            QPushButton:pressed {
                background-color: #D6D9DF;
            }
            
            QLineEdit {
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
            }
            
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
        """)
