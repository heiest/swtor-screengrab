from abc import ABC, abstractmethod
import os
import cv2
from typing import Tuple
from ahk import AHK
import swtor.global_data as global_data
import swtor.screenshot as screenshot
import time
import numpy
import swtor.template_match as template_match
import logging

class Window(ABC):
    template_base_path = 'ui-templates'
    tesseract_custom_config = r'-c tessedit_char_whitelist=",0123456789" --psm 7 --oem 3'
    training_base_path = 'training'

    def __init__(self, title, hotkey: str = None, logger = None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

        self._ahk = AHK()
        self._ahk_window = self._ahk.win_get(title = global_data.swtor_window_ahk_title)
        self.title = title
        self.hotkey = hotkey
        self.__template_path = os.path.join(Window.template_base_path, f'{self.title}.png')
        self.template = cv2.imread(self.__template_path, cv2.IMREAD_GRAYSCALE)
        self.__location = None

    @property
    @abstractmethod
    def _size(self):
        pass

    @property
    def visible(self) -> bool:
        match_strength, location = template_match.match_template_to_image(screenshot.take_game_window_screenshot(), self.template)
        if match_strength >= global_data.cv2_template_match_threshold:
            self.__location = location
            return True

        return False

    @property
    def location(self):
        if not self.__location:
            match_strength, location = template_match.match_template_to_image(screenshot.take_game_window_screenshot(), self.template)
            if match_strength >= global_data.cv2_template_match_threshold:
                self.__location = location
                self.logger.debug("Location is {self.__location}")
            else:
                return None

        return self.__location

    def _wait_for_visible(self):
        while not self.visible:
            time.sleep(1)