from abc import ABC, abstractmethod

class BaseConfig(ABC):
    def __init__(self, title: str):
        self.title = title

class LinearConfig(BaseConfig):
    def __init__(self, title: str, x_data: list, y_data: list):
        super().__init__(title)
        self.x = x_data
        self.y = y_data
    
class BarConfig(BaseConfig):
    def __init__(self, title: str, categories: list, values: list):
        super().__init__(title)
        self.categories = categories
        self.values = values
