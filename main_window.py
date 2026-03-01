from PySide6.QtWidgets import QFileDialog, QMainWindow, QSplitter
from PySide6.QtGui import QAction
from widgets.live_chart_widget import LiveChartWidget
from widgets.sidepanel_widget import SidePanel
from PySide6.QtCore import Qt
from json_gen.gen import save_config_to_json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,600)

        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        self.build_menu()

        # 3. Сreate SidePanel
        self.sidepanel_widget = SidePanel()
        self.live_chart_widget = LiveChartWidget()
        
        # 4. Add to Layout with Alignment
        self.splitter.addWidget(self.live_chart_widget)
        self.splitter.addWidget(self.sidepanel_widget)

        self.splitter.setSizes([700, 350])
        self.sidepanel_widget.setMinimumWidth(200)
        
        self.sidepanel_widget.request_chart_draw.connect(self.live_chart_widget.draw_chart)

        self.apply_styles()

    def build_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        save_action = QAction("Save As...", self)
        save_action.triggered.connect(self.save)

        export_action = QAction("Export to PNG", self)
        export_action.triggered.connect(self.export_png)

        file_menu.addActions([save_action, export_action])

    def save(self):
        config = self.sidepanel_widget.get_config()
        if config is None:
            return
        
        file_filter = "JSON File (*.json);;All Files(*.*)"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart Configuration", "chart_config.json", file_filter)

        if file_path:
            success = save_config_to_json(config, file_path)
            if success:
                print("Configuration file saved.")
            else:
                print("Failed to save configuration file.")

    def export_png(self):
        self.live_chart_widget.export_to_png()

    def apply_styles(self):
        self.setStyleSheet("""
            MainWindow {
                background-color: white;
            }

            QAction {
                color: black;
            }
        """)
