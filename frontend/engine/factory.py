from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from pandas.core.generic import ValueKeyFunc
from pandas.core.indexes.api import all_indexes_same
from pandas.io.parsers.base_parser import evaluate_callable_usecols

from config.config import BaseConfig, LineConfig, BarConfig

class BaseChart(ABC):
    def __init__(self, ax):
        self.ax = ax

    @abstractmethod
    def draw(self, config: BaseConfig):
        pass

class LineChart(BaseChart):
    def draw(self, config: LineConfig):
        marker = config.marker_style if config.marker_style != 'None' else ''

        self.ax.plot(
            config.x, 
            config.y, 
            color=config.color,
            linestyle=config.line_style,
            linewidth=config.line_width,
            marker=marker,
            markersize=config.marker_size,
            alpha=config.alpha
        )

        # Apply area fill under the line if checked
        if config.fill_under:
            self.ax.fill_between(
                config.x, 
                config.y, 
                color=config.color, 
                alpha=config.alpha * 0.3     
            )

        # Set labels and title with specific font sizes
        self.ax.set_title(config.title, fontsize=config.title_font_size)
        self.ax.set_xlabel(config.x_label, fontsize=config.axis_font_size)
        self.ax.set_ylabel(config.y_label, fontsize=config.axis_font_size)

        # Configure tick font sizes and rotation
        self.ax.tick_params(axis='both', which='major', labelsize=config.axis_font_size)
        if config.tick_rotation > 0:
            self.ax.tick_params(axis='x', rotation=config.tick_rotation)

        # Apply logarithmic scale
        if config.log_x:
            self.ax.set_xscale('log')
        if config.log_y:
            self.ax.set_yscale('log')

        # Safely apply axis limits if the user provided valid numbers
        if config.x_min.strip():
            try: 
                self.ax.set_xlim(left=float(config.x_min))
            except ValueError: 
                pass
                
        if config.x_max.strip():
            try: 
                self.ax.set_xlim(right=float(config.x_max))
            except ValueError: 
                pass
                
        if config.y_min.strip():
            try: 
                self.ax.set_ylim(bottom=float(config.y_min))
            except ValueError: 
                pass
                
        if config.y_max.strip():
            try: 
                self.ax.set_ylim(top=float(config.y_max))
            except ValueError: 
                pass

        # Apply grid
        self.ax.grid(config.is_grid)

        # Render legend if checked
        if config.show_legend:
            legend_label = config.title if config.title else "Data"
            self.ax.legend([legend_label], loc=config.legend_loc)

class BarChart(BaseChart):
    def draw(self, config: BarConfig):
        # Handle the 'None' string for edge color
        edge_color = config.edge_color if config.edge_color != 'None' else None

        # Draw the bar chart based on orientation
        if config.orientation == 'horizontal':
            self.ax.barh(
                y=config.categories, 
                width=config.values, 
                height=config.bar_width,
                color=config.color,
                edgecolor=edge_color,
                linewidth=config.edge_width,
                alpha=config.alpha
            )
        else:
            self.ax.bar(
                x=config.categories, 
                height=config.values, 
                width=config.bar_width,
                color=config.color,
                edgecolor=edge_color,
                linewidth=config.edge_width,
                alpha=config.alpha
            )

        # Set labels and title with specific font sizes
        self.ax.set_title(config.title, fontsize=config.title_font_size)
        self.ax.set_xlabel(config.x_label, fontsize=config.axis_font_size)
        self.ax.set_ylabel(config.y_label, fontsize=config.axis_font_size)

        # Configure tick font sizes and rotation
        self.ax.tick_params(axis='both', which='major', labelsize=config.axis_font_size)
        if config.tick_rotation > 0:
            # Rotate x-ticks for vertical, or y-ticks for horizontal to prevent overlap
            axis_to_rotate = 'x' if config.orientation == 'vertical' else 'y'
            self.ax.tick_params(axis=axis_to_rotate, rotation=config.tick_rotation)

        # Apply logarithmic scale
        if config.log_x:
            self.ax.set_xscale('log')
        if config.log_y:
            self.ax.set_yscale('log')

        # Safely apply axis limits if the user provided valid numbers
        if config.x_min.strip():
            try: 
                self.ax.set_xlim(left=float(config.x_min))
            except ValueError: 
                pass
                
        if config.x_max.strip():
            try: 
                self.ax.set_xlim(right=float(config.x_max))
            except ValueError: 
                pass
                
        if config.y_min.strip():
            try: 
                self.ax.set_ylim(bottom=float(config.y_min))
            except ValueError: 
                pass
                
        if config.y_max.strip():
            try: 
                self.ax.set_ylim(top=float(config.y_max))
            except ValueError: 
                pass

        # Apply grid (often useful only on one axis for bar charts, but we keep it general)
        self.ax.grid(config.is_grid)

        # Render legend if checked
        if config.show_legend:
            legend_label = config.title if config.title else "Data"
            self.ax.legend([legend_label], loc=config.legend_loc)


class ChartFactory:
    @staticmethod
    def create_chart(chart_type: str, ax) -> BaseChart:
        if chart_type == "Line Chart":
            return LineChart(ax)
        elif chart_type == "Bar Chart":
            return BarChart(ax)
        else:
            raise ValueError(f"Chart type '{chart_type}' is not supported.")
        
