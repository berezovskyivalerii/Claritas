from PySide6.QtWidgets import QFileDialog, QMainWindow, QTabWidget
from PySide6.QtGui import QAction
from widgets.chart_workspace_widget import ChartWorkspace 
from json_gen.gen import save_config_to_json
from json_gen.parse import parse_json_to_config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1400, 850)
        
        self.build_menu()
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Enable closing tabs
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Add the first default tab on startup
        self.add_new_tab("Default Chart")

        self.apply_styles()

    def build_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # Action to create a new tab
        new_tab_action = QAction("New Chart Tab", self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab("New Chart"))

        open_action = QAction("Open file", self)
        open_action.triggered.connect(self.open)

        save_action = QAction("Save As...", self)
        save_action.triggered.connect(self.save)

        export_action = QAction("Export to PNG", self)
        export_action.triggered.connect(self.export_png)

        file_menu.addActions([new_tab_action, open_action, save_action, export_action])

    def add_new_tab(self, title):
        # 1. Create a completely new, independent workspace
        new_workspace = ChartWorkspace()
        
        # 2. Add it to the QTabWidget
        self.tabs.addTab(new_workspace, title)
        
        # 3. Automatically switch focus to the newly created tab
        self.tabs.setCurrentWidget(new_workspace)

    def close_tab(self, index):
        # Optional: Prevent closing the very last tab
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open(self):
        file_filter = "JSON File (*.json);;All Files (*.*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File Configuration", ".", file_filter)

        if file_path:
            cfg = parse_json_to_config(file_path)
            if cfg:
                self.add_new_tab(cfg.title)
                current_workspace = self.tabs.currentWidget() 
                current_workspace.load(cfg)
                print("Successfuly parsed")
            else:
                print("Failed to parse")

    def save(self):
        # Dynamically fetch the workspace the user is currently looking at
        current_workspace = self.tabs.currentWidget()
        if not current_workspace:
            return

        # Delegate the data collection to the active workspace
        config = current_workspace.get_current_config()
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
        # Dynamically fetch the active workspace and trigger its export
        current_workspace = self.tabs.currentWidget()
        if current_workspace:
            current_workspace.export_current_chart()

    def apply_styles(self):
        self.setStyleSheet("""
            MainWindow {
                background-color: #F5F7FA;
            }

            QAction {
                color: black;
            }

            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
                border-radius: 4px;
                top: -1px; 
            }

            QTabBar {
                background-color: transparent;
            }

            QTabBar::tab {
                background-color: #E6E9ED;
                color: #666666;
                padding: 8px 16px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #CCCCCC;
                border-bottom: none; 
            }

            QTabBar::tab:hover {
                background-color: #D6D9DF;
                color: #333333;
            }

            QTabBar::tab:selected {
                background-color: #FFFFFF;
                color: #000000;
                font-weight: bold;
                margin-bottom: -1px; 
                padding-bottom: 9px;
            }
        """)
