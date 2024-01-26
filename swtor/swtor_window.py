from .window import Window
from ahk import AHK
import numpy
import math
import time
import swtor.global_data as global_data
from tkinter import Tk
import logging

class SwtorWindow(Window):
    default_mouse_speed = 10

    def __init__(self, logger = None):
        super(SwtorWindow, self).__init__(global_data.swtor_window_ahk_title, logger)
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

        self.__ahk = AHK()
        self.__ahk_window = self.__ahk.win_get(title = global_data.swtor_window_ahk_title)
        self.__location = None

    def __get_game_location(self, location):
        return (self.location[0] + location[0], self.location[1] + location[1])

    @property
    def _size(self):
        return (self.__ahk_window.rect[2], self.__ahk_window.rect[3])

    @property
    def location(self):
        if self.__location:
            return self.__location

        self.__location = (self.__ahk_window.rect[0], self.__ahk_window.rect[1])
        self.logger.debug(f'Location is {self.__location}')
        return self.__location

    def move_mouse(self, location, mouse_speed = default_mouse_speed):
        location_in_game = self.__get_game_location(location)
        self.__ahk.mouse_move(location_in_game[0], location_in_game[1], speed = mouse_speed, blocking = True)

    def activate(self):
        self.__ahk_window.activate()

    def send(self, keys):
        self.activate()
        self.__ahk.send(keys)

    def key_down(self, key):
        self.activate()
        self.__ahk.key_down(key)

    def key_up(self, key):
        self.activate()
        self.__ahk.key_up(key)

    def triple_click(self):
        self.click()
        self.click()
        self.click()

    def ctrl_c(self):
        self.send('{Ctrl down}c{Ctrl up}')
        self.send('{Ctrl down}c{Ctrl up}')

    @property
    def screen_center(self):
        screen_center_x = math.floor(self._size[0] / 2)
        screen_center_y = math.floor(self._size[1] / 2)
        return (screen_center_x, screen_center_y)

    def shift_click(self, location = None, mouse_speed = default_mouse_speed):
        if location is not None:
            self.move_mouse(location, mouse_speed)

        self.key_down('LShift')
        self.click()
        self.key_up('LShift')

    def right_click(self, location = None, mouse_speed = default_mouse_speed):
        if location is not None:
            self.move_mouse(location, mouse_speed)

        self.__ahk.right_click()

    def click(self, location = None, mouse_speed = default_mouse_speed):
        if location is not None:
            self.move_mouse(location, mouse_speed)

        self.__ahk.click()