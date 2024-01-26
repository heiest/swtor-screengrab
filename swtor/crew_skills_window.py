from .window import Window
import logging

class CrewSkillsWindow(Window):
    title = 'Crew Skills'
    hotkey = 'b'

    def __init__(self, logger = None):
        super(CrewSkillsWindow, self).__init__(CrewSkillsWindow.title, CrewSkillsWindow.hotkey, logger)
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

    @property
    def _size(self):
        pass