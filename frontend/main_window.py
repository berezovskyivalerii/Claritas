from PySide6.QtWidgets import QFileDialog, QMainWindow, QTabWidget
from PySide6.QtGui import QAction
from widgets import greeting_widget
from widgets.chart_workspace_widget import ChartWorkspace 
from json_gen.gen import save_config_to_json
from json_gen.parse import parse_json_to_config
from widgets.greeting_widget import GreetingWindow
from widgets.database_workspace_widget import DatabaseWorkspace

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
        greeting_window = GreetingWindow()
        
        # 2. Add it to the QTabWidget
        index = self.tabs.addTab(greeting_window, title)
        self.tabs.setCurrentIndex(index)

        greeting_window.fs_chosen.connect(lambda: self.replace_tab(greeting_window, "fs"))
        greeting_window.db_chosen.connect(lambda: self.replace_tab(greeting_window, "db"))

    def close_tab(self, index):
        if self.tabs.count() > 2:
            widget_to_remove = self.tabs.widget(index)
            self.tabs.removeTab(index)
            widget_to_remove.deleteLater()

    def replace_tab(self, old_widget, choice):
        index = self.tabs.indexOf(old_widget)
        if index == -1:
            return

        # Instantiate the correct workspace
        if choice == "fs":
            new_widget = ChartWorkspace()
            new_title = "Local CSV Chart"
        elif choice == "db":
            new_widget = DatabaseWorkspace() # Assuming you created this class
            new_title = "Database Chart"
        else:
            return

        # Replace the widget in the tab system
        self.tabs.removeTab(index)
        self.tabs.insertTab(index, new_widget, new_title)
        self.tabs.setCurrentIndex(index)
        
        # Delete the old greeting window to prevent memory leaks
        old_widget.deleteLater()

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
        # Postman light theme styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F9F9F9;
            }

            /* --- Menu Bar Styling --- */
            QMenuBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #EAEAEA;
                padding: 4px;
            }

            QMenuBar::item {
                background: transparent;
                padding: 6px 12px;
                color: #212121;
                border-radius: 4px;
                font-size: 13px;
            }

            QMenuBar::item:selected {
                background-color: #F2F2F2;
            }

            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #EAEAEA;
                border-radius: 4px;
                padding: 4px 0px;
            }

            QMenu::item {
                padding: 6px 24px 6px 24px;
                color: #212121;
                font-size: 13px;
            }

            QMenu::item:selected {
                background-color: #F2F2F2;
            }

            /* --- Tab Widget Styling --- */
            QTabWidget::pane {
                border: 1px solid #EAEAEA;
                background-color: #FFFFFF;
                border-radius: 6px;
                margin-top: 0px;
            }

            QTabBar {
                background-color: transparent;
            }

            QTabBar::tab {
                background-color: transparent;
                color: #6B6B6B;
                padding: 10px 20px;
                border: none;
                border-bottom: 2px solid transparent; 
                font-size: 13px;
                font-weight: 500;
            }

            QTabBar::tab:hover {
                color: #212121;
                background-color: #F2F2F2;
            }

            QTabBar::tab:selected {
                color: #212121;
                background-color: #FFFFFF;
                border-bottom: 2px solid #3B82F6; /* Postman signature orange accent */
                font-weight: bold;
            }

            /* --- Tab Close Button Styling --- */
            QTabBar::close-button {
                background: transparent;
                padding: 2px;
            }

            QTabBar::close-button:hover {
                background-color: #EAEAEA;
                border-radius: 2px;
            }
        """)
