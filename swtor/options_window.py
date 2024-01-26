from .window import Window
import logging

class OptionsWindow(Window):
    title = 'Options'
    def __init__(self, logger = None):
        super(OptionsWindow, self).__init__(OptionsWindow.title, logger)
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

    @property
    def _size(self):
        pass