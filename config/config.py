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

    @classmethod
    def from_dict(cls, data: dict, raw_x: list, raw_y: list):
        return cls(
            path=data.get("path", ""),
            title=data.get("title", ""),
            x_data=raw_x,
            y_data=raw_y,
            x_label=data.get("x_label", ""),
            y_label=data.get("y_label", ""),
            color=data.get("color", "blue"),
            is_grid=data.get("is_grid", False)
        )
    
class BarConfig(BaseConfig):
    exclude_from_save = ["categories", "values"]

    def __init__(self, path: str, title: str, categories: list, values: list, x_label: str, y_label: str):
        super().__init__(title)
        self.path = path
        self.chart_type = "bar"
        self.categories = categories
        self.values = values
        self.x_label = x_label
        self.y_label = y_label

    @classmethod
    def from_dict(cls, data: dict, raw_categories: list, raw_values: list):
        return cls(
            path=data.get("path", ""),
            title=data.get("title", ""),
            categories=raw_categories,
            values=raw_values,
            x_label=data.get("x_label", ""),
            y_label=data.get("y_label", "")
        )
