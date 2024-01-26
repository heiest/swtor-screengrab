from .slotted_window import SlottedWindow
import numpy
import cv2
from .window import Window
import os
import logging

class InventoryWindow(SlottedWindow):
    title = 'Inventory'
    hotkey = 'i'

    def __init__(self, logger = None):
        super(InventoryWindow, self).__init__(InventoryWindow.title, InventoryWindow.hotkey, logger)
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

    @property
    def _size(self):
        return (614, 667)

    @property
    def _first_slot_offset(self):
        return numpy.array((50, 179))

    @property
    def _last_slot_offset(self):
        return numpy.array((570, 587))

    @property
    def _empty_slot_template(self):
        return cv2.imread(os.path.join(Window.template_base_path, 'Empty Inventory Slot.png'), cv2.IMREAD_GRAYSCALE)