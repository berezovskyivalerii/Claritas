from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QHBoxLayout, QVBoxLayout
from widgets.live_chart_widget import LiveChartWidget
from widgets.sidepanel_widget import SidePanel
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.setStyleSheet("background-color: white;")

        self.splitter = QSplitter(Qt.Horizontal)

        self.setCentralWidget(self.splitter)
        # 3. Сreate SidePanel
        self.sidepanel_widget = SidePanel()
        self.live_chart_widget = LiveChartWidget()
        
        # 4. Add to Layout with Alignment
        self.splitter.addWidget(self.live_chart_widget)
        self.splitter.addWidget(self.sidepanel_widget)

        self.splitter.setSizes([700, 350])
        self.sidepanel_widget.setMinimumWidth(200)

        self.sidepanel_widget.request_chart_draw.connect(self.live_chart_widget.draw_chart)

