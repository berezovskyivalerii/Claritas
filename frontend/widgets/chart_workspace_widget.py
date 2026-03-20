from PySide6.QtWidgets import QSplitter
from PySide6.QtCore import Qt
from widgets.live_chart_widget import LiveChartWidget
from widgets.sidepanel_widget import SidePanel

class ChartWorkspace(QSplitter):
    def __init__(self):
        super().__init__(Qt.Horizontal)

        # 1. Initialize child widgets specifically for this workspace
        self.sidepanel_widget = SidePanel("filesystem")
        self.live_chart_widget = LiveChartWidget()
        
        # 2. Add widgets to the splitter
        self.addWidget(self.live_chart_widget)
        self.addWidget(self.sidepanel_widget)

        # 3. Set sizes and limits
        self.setSizes([700, 350])
        self.sidepanel_widget.setMinimumWidth(200)

        # 4. Internal signal routing: completely isolated from other tabs
        self.sidepanel_widget.request_chart_draw.connect(self.live_chart_widget.draw_chart)

    # Expose methods to be called by MainWindow menus
    def get_current_config(self):
        return self.sidepanel_widget.get_config()

    def export_current_chart(self):
        self.live_chart_widget.export_to_png()

    def load(self, cfg):
        self.sidepanel_widget.load(cfg)
