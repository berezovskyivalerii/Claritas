from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QVBoxLayout, QWidget
from engine.factory import ChartFactory

class LiveChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) 

        self.layout = QVBoxLayout(self)
        
        # Initialize Matplotlib Figure and Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Create the empty methematical axes
        self.ax = self.figure.add_subplot(111)

    def draw_chart(self, chart_type: str, config):
        self.ax.clear() 

        chart_strategy = ChartFactory.create_chart(chart_type, self.ax)
        chart_strategy.draw(config)

        self.canvas.draw()

    def export_to_png(self):
        file_filter = "PNG Image (*.png);;JPEG Image (*.jpg);;All Files(*.*)"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart As", "chart.png", file_filter)

        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                print(f"Export Successful: {file_path}")
            except Exception as e:
                print(f"Failed to export chart: {e}")
