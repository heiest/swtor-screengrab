from .error import Error
from .window import Window

class WindowNotFoundError(Error):
    def __init__(self, window: Window):
        self.window = window