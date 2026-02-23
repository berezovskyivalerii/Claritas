from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from pandas.core.generic import ValueKeyFunc
from pandas.core.indexes.api import all_indexes_same
from pandas.io.parsers.base_parser import evaluate_callable_usecols

from config.config import BaseConfig, LinearConfig, BarConfig

class BaseChart(ABC):
    def __init__(self, ax):
        self.ax = ax

    @abstractmethod
    def draw(self, config: BaseConfig):
        pass

class LineChart(BaseChart):
    def draw(self, config: LinearConfig):
        self.ax.plot(config.x, config.y, marker="o", color="blue")
        self.ax.set_title(config.title)
        self.ax.grid(True)

class BarChart(BaseChart):
    def draw(self, config: BarConfig):
        self.ax.bar(config.categories, config.values, color="green")
        self.ax.set_title(config.title)

class ChartFactory:
    @staticmethod
    def create_chart(chart_type: str, ax) -> BaseChart:
        if chart_type == "line":
            return LineChart(ax)
        elif chart_type == "bar":
            return BarChart(ax)
        else:
            raise ValueError(f"Chart type '{chart_type}' is not supported.")
        
