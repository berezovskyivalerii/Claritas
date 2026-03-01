from abc import ABC

class BaseConfig(ABC):
    exlude_from_save = []

    def __init__(self, title: str):
        self.title = title

    def to_saveable_dict(self):
        data = self.__dict__.copy()

        for key in self.exlude_from_save:
            data.pop(key)

        return data

class LineConfig(BaseConfig):
    exlude_from_save = ["x", "y"]

    def __init__(self, path: str, title: str, x_data: list, y_data: list, x_label: str, y_label: str, color: str, is_grid: bool):
        super().__init__(title)
        self.chart_type = "line"
        self.path = path
        self.x = x_data
        self.y = y_data
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.is_grid = is_grid
    
class BarConfig(BaseConfig):
    exlude_from_save = ["categories", "values"]

    def __init__(self, path: str, title: str, categories: list, values: list, x_label: str, y_label: str):
        super().__init__(title)
        self.path = path
        self.chart_type = "bar"
        self.categories = categories
        self.values = values
        self.x_label = x_label
        self.y_label = y_label

