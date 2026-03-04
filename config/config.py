from abc import ABC

class BaseConfig(ABC):
    exclude_from_save = []

    def __init__(self, title: str):
        self.title = title

    def to_saveable_dict(self):
        data = self.__dict__.copy()

        for key in self.exclude_from_save:
            data.pop(key)

        return data

class LineConfig(BaseConfig):
    exclude_from_save = ["x", "y"]

    def __init__(self, path: str, title: str, x_data: list, y_data: list, 
                 x_label: str, y_label: str, color: str, is_grid: bool,
                 line_style: str = "solid", line_width: float = 1.5,
                 marker_style: str = "None", marker_size: int = 5,
                 x_min: str = "", x_max: str = "", y_min: str = "", y_max: str = "",
                 log_x: bool = False, log_y: bool = False, tick_rotation: int = 0,
                 show_legend: bool = False, legend_loc: str = "best",
                 fill_under: bool = False, alpha: float = 1.0,
                 title_font_size: int = 12, axis_font_size: int = 10):
        super().__init__(title)
        self.chart_type = "line"
        self.path = path
        self.x = x_data
        self.y = y_data
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.is_grid = is_grid
        
        # Extended visual properties
        self.line_style = line_style
        self.line_width = line_width
        self.marker_style = marker_style
        self.marker_size = marker_size
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.log_x = log_x
        self.log_y = log_y
        self.tick_rotation = tick_rotation
        self.show_legend = show_legend
        self.legend_loc = legend_loc
        self.fill_under = fill_under
        self.alpha = alpha
        self.title_font_size = title_font_size
        self.axis_font_size = axis_font_size

    @classmethod
    def from_dict(cls, data: dict, raw_x: list, raw_y: list):
        # Extract data with safe fallbacks for backward compatibility
        return cls(
            path=data.get("path", ""),
            title=data.get("title", ""),
            x_data=raw_x,
            y_data=raw_y,
            x_label=data.get("x_label", ""),
            y_label=data.get("y_label", ""),
            color=data.get("color", "Blue"),
            is_grid=data.get("is_grid", False),
            line_style=data.get("line_style", "solid"),
            line_width=data.get("line_width", 1.5),
            marker_style=data.get("marker_style", "None"),
            marker_size=data.get("marker_size", 5),
            x_min=data.get("x_min", ""),
            x_max=data.get("x_max", ""),
            y_min=data.get("y_min", ""),
            y_max=data.get("y_max", ""),
            log_x=data.get("log_x", False),
            log_y=data.get("log_y", False),
            tick_rotation=data.get("tick_rotation", 0),
            show_legend=data.get("show_legend", False),
            legend_loc=data.get("legend_loc", "best"),
            fill_under=data.get("fill_under", False),
            alpha=data.get("alpha", 1.0),
            title_font_size=data.get("title_font_size", 12),
            axis_font_size=data.get("axis_font_size", 10)
        )
    
class BarConfig(BaseConfig):
    exclude_from_save = ["categories", "values"]

    def __init__(self, path: str, title: str, categories: list, values: list, 
                 x_label: str, y_label: str, color: str = "Blue", is_grid: bool = False,
                 orientation: str = "vertical", bar_width: float = 0.8,
                 edge_color: str = "None", edge_width: float = 0.0, alpha: float = 1.0,
                 x_min: str = "", x_max: str = "", y_min: str = "", y_max: str = "",
                 log_x: bool = False, log_y: bool = False, tick_rotation: int = 0,
                 show_legend: bool = False, legend_loc: str = "best",
                 title_font_size: int = 12, axis_font_size: int = 10):
        super().__init__(title)
        self.chart_type = "bar"
        self.path = path
        self.categories = categories
        self.values = values
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.is_grid = is_grid
        
        # Extended visual properties for bar charts
        self.orientation = orientation
        self.bar_width = bar_width
        self.edge_color = edge_color
        self.edge_width = edge_width
        self.alpha = alpha
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.log_x = log_x
        self.log_y = log_y
        self.tick_rotation = tick_rotation
        self.show_legend = show_legend
        self.legend_loc = legend_loc
        self.title_font_size = title_font_size
        self.axis_font_size = axis_font_size

    @classmethod
    def from_dict(cls, data: dict, raw_categories: list, raw_values: list):
        # Extract data with safe fallbacks for backward compatibility
        return cls(
            path=data.get("path", ""),
            title=data.get("title", ""),
            categories=raw_categories,
            values=raw_values,
            x_label=data.get("x_label", ""),
            y_label=data.get("y_label", ""),
            color=data.get("color", "Blue"),
            is_grid=data.get("is_grid", False),
            orientation=data.get("orientation", "vertical"),
            bar_width=data.get("bar_width", 0.8),
            edge_color=data.get("edge_color", "None"),
            edge_width=data.get("edge_width", 0.0),
            alpha=data.get("alpha", 1.0),
            x_min=data.get("x_min", ""),
            x_max=data.get("x_max", ""),
            y_min=data.get("y_min", ""),
            y_max=data.get("y_max", ""),
            log_x=data.get("log_x", False),
            log_y=data.get("log_y", False),
            tick_rotation=data.get("tick_rotation", 0),
            show_legend=data.get("show_legend", False),
            legend_loc=data.get("legend_loc", "best"),
            title_font_size=data.get("title_font_size", 12),
            axis_font_size=data.get("axis_font_size", 10)
        )
