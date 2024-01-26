from .slotted_window import SlottedWindow
import numpy
import cv2
from .window import Window
import os
import logging

class CargoHoldWindow(SlottedWindow):
    title = 'Cargo Hold'

    def __init__(self, logger = None):
        super(CargoHoldWindow, self).__init__(CargoHoldWindow.title, logger)
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

    @property
    def _size(self):
        return (606, 610)

    @property
    def _first_slot_offset(self):
        return numpy.array((42, 96))

    @property
    def _last_slot_offset(self):
        return numpy.array((558, 506))

    @property
    def _empty_slot_template(self):
        return cv2.imread(os.path.join(Window.template_base_path, 'Empty Cargo Hold Slot.png'), cv2.IMREAD_GRAYSCALE)