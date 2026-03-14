from PySide6.QtWidgets import QStackedWidget, QWidget, QPushButton, QVBoxLayout, QFileDialog, QComboBox, QLabel
from PySide6.QtCore import Qt, Signal
from config.config import BaseConfig, LineConfig
from widgets.bar_settings_widget import BarSettingsWidget
from widgets.line_settings_widget import LineSettingsWidget
from client import  GrpcDataStreamer
import grpc
from api import claritas_pb2
from api import claritas_pb2_grpc

class SidePanel(QWidget):
    request_chart_draw = Signal(str, object)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) 

        self.raw_x = []
        self.raw_y = []
        self.chart_type = "Line Chart"
        self.selected_path = ""
        self.streamer = None

        # --- Create Main Layout --- 
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.upload_button = QPushButton("Upload Data File")
        self.upload_button.setObjectName("uploadButton")
        self.upload_button.clicked.connect(self.select_file)

        # --- Axis Selection UI ---
        self.x_label = QLabel("X Axis Column:")
        self.x_combo = QComboBox()
        self.y_label = QLabel("Y Axis Column:")
        self.y_combo = QComboBox()
        
        # Connect changes in comboboxes to the parsing trigger
        self.x_combo.currentIndexChanged.connect(self.trigger_parsing)
        self.y_combo.currentIndexChanged.connect(self.trigger_parsing)

        # Create the ComboBox for Chart Type
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
        self.submit_button.setObjectName("submitButton")
        self.submit_button.clicked.connect(self.get_user_data)

        # Add everything to the main layout
        self.main_layout.addWidget(self.upload_button)
        self.main_layout.addWidget(self.x_label)  # New X label
        self.main_layout.addWidget(self.x_combo)  # New X combo
        self.main_layout.addWidget(self.y_label)  # New Y label
        self.main_layout.addWidget(self.y_combo)  # New Y combo
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

    def load(self, cfg):
        self.selected_path = cfg.path
        
        self.combo_box.blockSignals(True)
        
        if cfg.chart_type == 'line':
            self.chart_type = 'Line Chart'
            self.raw_x = cfg.x
            self.raw_y = cfg.y
            self.combo_box.setCurrentIndex(0)
            self.stacked_widget.setCurrentIndex(0)

            self.line_settings.load_ui(cfg)
            
        elif cfg.chart_type == 'bar':
            self.chart_type = 'Bar Chart'
            self.raw_x = cfg.categories
            self.raw_y = cfg.values
            self.combo_box.setCurrentIndex(1)
            self.stacked_widget.setCurrentIndex(1)

            self.bar_settings.load_ui(cfg)

        self.combo_box.blockSignals(False)

        self.request_chart_draw.emit(self.chart_type, cfg)


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
            self.fetch_headers_only(self.selected_path)

    # 1. Fetch headers and populate combo boxes
    def fetch_headers_only(self, path):
        channel = grpc.insecure_channel('unix:///tmp/claritas.sock')
        stub = claritas_pb2_grpc.ClaritasEngineStub(channel)
        
        try:
            req = claritas_pb2.FileRequest(file_path=path)
            res = stub.GetHeaders(req)
            headers = list(res.columns)
            
            if len(headers) < 2:
                print("Error: CSV must contain at least 2 columns")
                return

            # Block signals temporarily so adding items doesn't trigger parsing multiple times
            self.x_combo.blockSignals(True)
            self.y_combo.blockSignals(True)
            
            self.x_combo.clear()
            self.y_combo.clear()
            
            self.x_combo.addItems(headers)
            self.y_combo.addItems(headers)

            # Set default selection (column 0 for X, column 1 for Y)
            self.x_combo.setCurrentIndex(0)
            self.y_combo.setCurrentIndex(1)
            
            # Unblock signals
            self.x_combo.blockSignals(False)
            self.y_combo.blockSignals(False)

            # Manually trigger the first parse with the default columns
            self.trigger_parsing()

        except grpc.RpcError as e:
            print(f"Failed to get headers: {e.details()}")
        finally:
            channel.close()

    # 2. Trigger parsing based on selected combo box values
    def trigger_parsing(self):
        if not self.selected_path:
            return

        x_col_name = self.x_combo.currentText()
        y_col_name = self.y_combo.currentText()

        if not x_col_name or not y_col_name:
            return

        # Clear old data
        self.raw_x = []
        self.raw_y = []
        
        # Disable UI elements to prevent user from interrupting the stream
        self.upload_button.setEnabled(False)
        self.submit_button.setEnabled(False)
        self.x_combo.setEnabled(False)
        self.y_combo.setEnabled(False)
        self.upload_button.setText("Loading...")

        # Start asynchronous streaming
        self.streamer = GrpcDataStreamer(self.selected_path, x_col_name, y_col_name)
        self.streamer.chunk_received.connect(self.on_chunk_received)
        self.streamer.error_occurred.connect(self.on_streaming_error)
        self.streamer.finished.connect(self.on_streaming_finished)
        self.streamer.start()

    def on_chunk_received(self, x_chunk, y_chunk):
        self.raw_x.extend(x_chunk)
        self.raw_y.extend(y_chunk)

    def on_streaming_error(self, error_msg):
        print(f"Streaming Error: {error_msg}")

    def on_streaming_finished(self):
        # Re-enable UI elements after parsing is complete
        self.upload_button.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.x_combo.setEnabled(True)
        self.y_combo.setEnabled(True)
        self.upload_button.setText("Upload Data File")
        
        print(f"Successfully loaded {len(self.raw_x)} rows via gRPC")
        
        self.get_user_data() 

    def apply_styles(self):
        # Keep your existing styles
        self.setStyleSheet("""
            SidePanel {
                background-color: #F5F7FA;
            }

            QComboBox {
                color: black;
                background-color: white;
            }
            
            #uploadButton {
                padding: 5px 0px;
                border-radius: 5px;
                background-color: #4681f4;
                color: #FFFFFF;
                border: 1px solid #3A7CBD;
                font: bold;
            }
            
            #uploadButton:hover {
                background-color: #3A7CBD;
            }
            
            #uploadButton:pressed {
                background-color: #2C5F96;
            }
            
            #submitButton {
                padding: 10px 0px;
                background-color: #33b249;
                color: #FFFFFF;
                border: 1px solid #27AE60;
                font-weight: bold;
                font-size: 16px;
            }
            
            #submitButton:hover {
                background-color: #27AE60;
            }
            
            #submitButton:pressed {
                background-color: #1E8449;
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
