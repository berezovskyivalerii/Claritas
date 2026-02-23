from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget
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
