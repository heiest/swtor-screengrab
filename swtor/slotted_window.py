from .window import Window
import swtor.screenshot as screenshot
from abc import ABC, abstractmethod
import numpy
import math
import os
import cv2
import os
import swtor.template_match as template_match
import logging

class SlottedWindow(Window, ABC):
    slot_size = numpy.array((57.2, 58.125)) # Measured to **outer edges** of slots, divided by slot count in X and Y
    def __init__(self, title, hotkey: str = None, logger = None):
        super(SlottedWindow, self).__init__(title, hotkey, logger)
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

    @property
    @abstractmethod
    def _empty_slot_template(self):
        pass

    @property
    @abstractmethod
    def _first_slot_offset(self):
        pass

    @property
    @abstractmethod
    def _last_slot_offset(self):
        pass

    @property
    def _slot_count(self):
        first_last_slot_diff = numpy.array(self._last_slot_offset) - numpy.array(self._first_slot_offset)
        slot_count = (first_last_slot_diff / SlottedWindow.slot_size) + (1, 1) # First and last slot offsets are to the **center** of the slot, so our count will be short by 1; add 1 to both X and Y
        return numpy.rint(slot_count).astype(int)

    @property
    def slot_locations(self):
        self._wait_for_visible()
        locations = list()
        window_location = numpy.array(self.location)
        first_slot_location = window_location + self._first_slot_offset
        last_slot_location = window_location + self._last_slot_offset
        first_empty_slot_location = self.__first_empty_slot_location
        end_slot_location_exclusive = first_empty_slot_location + window_location if first_empty_slot_location is not None else numpy.array(self.location) + numpy.array(self._size)
        for y in range(self._slot_count[1]):
            for x in range(self._slot_count[0]):
                location = first_slot_location + (SlottedWindow.slot_size * (x, y))
                if (location[1] < end_slot_location_exclusive[1] or
                    location[0] < end_slot_location_exclusive[0]):
                    locations.append((math.floor(location[0]), math.floor(location[1])))
                else:
                    return locations

        return locations

    @property
    def __first_empty_slot_location(self):
        self._wait_for_visible()
        inventory_window_rect = (
            self.location[0],
            self.location[1],
            self._size[0],
            self._size[1])
        locations = template_match.match_template_to_image_multiple_occurrences(screenshot.take_game_window_partial_screenshot(inventory_window_rect), self._empty_slot_template)
        z = numpy.array(list(zip(*locations[::-1])))
        if not z.any():
            return None
        ind = numpy.lexsort((z[:,0],z[:,1]))
        return z[ind][0]