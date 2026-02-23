from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from widgets.live_chart_widget import LiveChartWidget
from widgets.sidepanel_widget import SidePanel
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        # 1. Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet('background-color: white')

        # 2. Main Horizontal Layout
        main_layout = QHBoxLayout(central_widget)
        
        # 3. Сreate SidePanel
        self.sidepanel_widget = SidePanel()
        self.sidepanel_widget.setFixedWidth(350) # TODO

        self.live_chart_widget = LiveChartWidget()
        self.live_chart_widget.setFixedWidth(700) # TODO
        
        # 4. Add to Layout with Alignment
        main_layout.addWidget(self.live_chart_widget, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.sidepanel_widget, alignment=Qt.AlignRight)

        self.sidepanel_widget.image_generated.connect(self.live_chart_widget.update_live_data)

