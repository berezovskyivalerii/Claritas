from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PySide6.QtCore import QFile, Qt, Signal
import pandas
from config.config import LinearConfig

class SidePanel(QWidget):
    image_generated = Signal(LinearConfig)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) 

        # Create Config Instance
        self.cfg = LinearConfig()

        # --- Create Main Layout --- 
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        
        # --- Upload Button ---
        self.upload_button = QPushButton("Upload Data File")
        self.upload_button.clicked.connect(self.select_file)

        # --- Title Input ---
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Input chart title...")
        
        # --- X & Y Label Inputs ---
        self.x_label_input = QLineEdit()
        self.x_label_input.setPlaceholderText("Input X label...")
  
        self.y_label_input = QLineEdit()
        self.y_label_input.setPlaceholderText("Input Y label...")
        
        # --- Submit Button ---
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.get_user_data)

        # --- Add Widgets ---
        self.main_layout.addWidget(self.upload_button)
        self.main_layout.addWidget(self.title_input)
        self.main_layout.addWidget(self.x_label_input)
        self.main_layout.addWidget(self.y_label_input)
        self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)

        # --- Styles ---
        self.apply_styles()

    # Read inputs
    def get_user_data(self):
        title = self.title_input.text()
        x_label = self.x_label_input.text()
        y_label = self.y_label_input.text()

        self.cfg.title = title
        self.cfg.x_label = x_label
        self.cfg.y_label = y_label

        self.image_generated.emit(self.cfg)

    # Select .csv file
    def select_file(self):
        dialog_filter = "CSV filter (*.csv);;All files (*.*)"

        selected_path, _ = QFileDialog.getOpenFileName(None, "Select Data File", "", dialog_filter)
        if selected_path: 
            self.parse_selected_file(selected_path)

    # Parse file to config
    def parse_selected_file(self, path):
        # read only first and second column
        data_df = pandas.read_csv(path, usecols=[0,1])

        self.cfg.x = data_df.iloc[:, 0].tolist()
        self.cfg.y = data_df.iloc[:, 1].tolist()
        
        # TODO: Check if amount of values is the same

    def apply_styles(self):
        self.setStyleSheet("""
            SidePanel {
                background-color: #F5F7FA;
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
