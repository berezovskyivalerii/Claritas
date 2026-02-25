from abc import ABC, abstractmethod

class BaseConfig(ABC):
    def __init__(self, title: str):
        self.title = title

class LineConfig(BaseConfig):
    def __init__(self, title: str, x_data: list, y_data: list, x_label: str, y_label: str):
        super().__init__(title)
        self.x = x_data
        self.y = y_data
        self.x_label = x_label
        self.y_label = y_label
    
class BarConfig(BaseConfig):
    def __init__(self, title: str, categories: list, values: list, x_label: str, y_label: str):
        super().__init__(title)
        self.categories = categories
        self.values = values
        self.x_label = x_label
        self.y_label = y_label

