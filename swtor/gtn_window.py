from .window import Window
import swtor.screenshot as screenshot
import numpy
import os
import cv2
import swtor.global_data as global_data
import pytesseract
from .ocr_error import OcrError
import uuid
from tkinter import Tk
import time
import re
from .swtor_window import SwtorWindow
from .gtn_results_page import GtnResultsPage
import swtor.template_match as template_match
import logging

class GtnWindow(Window):
    title = 'Galactic Trade Network'
    unit_price_ascending_template_match_threshold = 0.99

    def __init__(self, logger = None):
        super(GtnWindow, self).__init__(GtnWindow.title, logger)
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

        self.__swtor_window = SwtorWindow()
        self.__search_button_offset = (116, 567)
        self.__search_box_offset = (116, 92)
        self.__unit_price_column_header_offset = (944, 78)
        self.__reset_button_offset = (237, 567)
        self.__unit_price_ascending_template = cv2.imread(os.path.join(Window.template_base_path, 'Unit Price Ascending.png'), cv2.IMREAD_GRAYSCALE)
        self.__no_results_template = cv2.imread(os.path.join(Window.template_base_path, 'No Results.png'), cv2.IMREAD_GRAYSCALE)
        self.__page_template = cv2.imread(os.path.join(Window.template_base_path, 'Page.png'), cv2.IMREAD_GRAYSCALE)
        self.__next_page_template = cv2.imread(os.path.join(Window.template_base_path, 'Next Page.png'), cv2.IMREAD_GRAYSCALE)
        self.__previous_page_template = cv2.imread(os.path.join(Window.template_base_path, 'Previous Page.png'), cv2.IMREAD_GRAYSCALE)
        self.__next_page_button_offset = (12, 12)
        self.__has_results = None
        self.is_sorted_ascending = False

    @property
    def __search_button_location(self):
        return numpy.array(self.location) + numpy.array(self.__search_button_offset)

    @property
    def _size(self):
        return (1157, 661)

    @property
    def rect(self):
        window_location = numpy.array(self.location)
        return (
            window_location[0],
            window_location[1],
            self._size[0],
            self._size[1])

    def __click_next_page(self):
        match_strength, next_page_location = template_match.match_template_to_image(screenshot.take_game_window_partial_screenshot(self.rect), self.__next_page_template)
        if match_strength < global_data.cv2_template_match_threshold:
            return

        self.__swtor_window.click(numpy.array(self.location) + numpy.array(next_page_location) + numpy.array(self.__next_page_button_offset))

    def lowest_price(self, item_name):
        if not self.has_results:
            return None

        price = None
        while True:
            results = GtnResultsPage(self)
            price = results.lowest_price(item_name)
            if price:
                break

            current_page, page_count = self.__page
            if current_page == page_count:
                break

            self.__click_next_page()

        return price

    def results(self, item_name):
        if not self.has_results:
            return None

        results = None
        while True:
            page_results = GtnResultsPage(self).results(item_name)
            if page_results is not None:
                if results is None:
                    results = []

                results.extend(page_results)

            current_page, page_count = self.__page
            if current_page == page_count:
                break

            self.__click_next_page()
            self.__swtor_window.move_mouse(self.location)

        return results

    @property
    def __page(self):
        if not self.has_results:
            return None

        # KE: subtract a bit from the width so as to exclude the text "Go To Page:"
        # in the lower-right corner of the GTN window. This will ensure that the
        # "Page: " template search finds the correct instance.
        narrow_self_rect = (
            self.rect[0],
            self.rect[1],
            self.rect[2] - 250,
            self.rect[3]
        )
        match_strength, page_template_location = template_match.match_template_to_image(screenshot.take_game_window_partial_screenshot(narrow_self_rect), self.__page_template)
        if match_strength < global_data.cv2_template_match_threshold:
            return None

        page_template_width = self.__page_template.shape[1]
        page_rect = (
            self.location[0] + page_template_location[0],
            self.location[1] + page_template_location[1],
            self.__page_template.shape[1] + 200,
            self.__page_template.shape[0]
        )
        image = screenshot.take_game_window_partial_screenshot_ocr(page_rect)
        page_string = pytesseract.image_to_string(image).strip()
        regex_match = re.search(r'(?<=Page:\s)(\d+)/(\d+)', page_string)
        return (int(regex_match.group(1)), int(regex_match.group(2)))

    @property
    def has_results(self) -> bool:
        if self.__has_results is None:
            match_strength, location = template_match.match_template_to_image(screenshot.take_game_window_partial_screenshot(self.rect), self.__no_results_template)
            if match_strength >= global_data.cv2_template_match_threshold:
                self.__has_results = False
            else:
                self.__has_results = True

        return self.__has_results

    def search(self):
        self.__swtor_window.click(self.__search_button_location)
        self.__swtor_window.move_mouse(self.location)
        self.__has_results = None

    @property
    def searched_item_name(self):
        self.__swtor_window.move_mouse(self.__search_box_location)
        self.__swtor_window.click()
        self.__swtor_window.ctrl_c()
        item_name = Tk().clipboard_get()
        return item_name

    def __click_unit_price_column_header(self):
        self.__swtor_window.click(self.__unit_price_column_header_location)
        self.__swtor_window.move_mouse(self.location)

    def sort_by_unit_price_ascending(self):
        results = GtnResultsPage(self)
        if results.result_count <= 1:
            return

        # KE: sometimes the GTN window shows as being sorted by unit price ascending
        # but it is not. So do an unconditional click on the column header to
        # "jiggle the handle" and then do the check to see if properly sorted.
        self.__click_unit_price_column_header()
        while not self.__unit_price_sorted_ascending:
            self.__click_unit_price_column_header()

    @property
    def __search_box_location(self):
        return numpy.array(self.location) + numpy.array(self.__search_box_offset)

    @property
    def __unit_price_column_header_location(self):
        return numpy.array(self.location) + numpy.array(self.__unit_price_column_header_offset)

    @property
    def __reset_button_location(self):
        return numpy.array(self.location) + numpy.array(self.__reset_button_offset)

    @property
    def __unit_price_sorted_ascending(self) -> bool:
        unit_price_rect = (
            self.__unit_price_column_header_location[0] - 100,
            self.__unit_price_column_header_location[1] - 50,
            200,
            100)
        match_strength, location = template_match.match_template_to_image(screenshot.take_game_window_partial_screenshot(unit_price_rect), self.__unit_price_ascending_template)
        if match_strength >= GtnWindow.unit_price_ascending_template_match_threshold:
            return True

        return False

