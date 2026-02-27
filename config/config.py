from abc import ABC

class BaseConfig(ABC):
    def __init__(self, title: str):
        self.title = title

class LineConfig(BaseConfig):
    def __init__(self, title: str, x_data: list, y_data: list, x_label: str, y_label: str, color: str, is_grid: bool):
        super().__init__(title)
        self.x = x_data
        self.y = y_data
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.is_grid = is_grid
    
class BarConfig(BaseConfig):
    def __init__(self, title: str, categories: list, values: list, x_label: str, y_label: str):
        super().__init__(title)
        self.categories = categories
        self.values = values
        self.x_label = x_label
        self.y_label = y_label

