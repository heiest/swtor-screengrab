import swtor.screenshot as screenshot
import pytesseract
from .window import Window
import re

class GtnSearchResult():
    _height = 58
    _first_offset = 93
    _first_name_rect = (352, _first_offset, 195, _height)
    _first_time_rect = (612, _first_offset, 60, _height)
    _first_seller_rect = (672, _first_offset, 100, _height)
    _first_unit_price_rect = (916, _first_offset, 110, _height)
    _lokath = r'lokath'

    def __init__(self, gtn_window_screenshot, index):
        name_rect = (
            GtnSearchResult._first_name_rect[0],
            GtnSearchResult._first_name_rect[1] + GtnSearchResult._height * index,
            GtnSearchResult._first_name_rect[2],
            GtnSearchResult._first_name_rect[3]
        )
        time_rect = (
            GtnSearchResult._first_time_rect[0],
            GtnSearchResult._first_time_rect[1] + GtnSearchResult._height * index,
            GtnSearchResult._first_time_rect[2],
            GtnSearchResult._first_time_rect[3]
        )
        seller_rect = (
            GtnSearchResult._first_seller_rect[0],
            GtnSearchResult._first_seller_rect[1] + GtnSearchResult._height * index,
            GtnSearchResult._first_seller_rect[2],
            GtnSearchResult._first_seller_rect[3]
        )
        unit_price_rect = (
            GtnSearchResult._first_unit_price_rect[0],
            GtnSearchResult._first_unit_price_rect[1] + GtnSearchResult._height * index,
            GtnSearchResult._first_unit_price_rect[2],
            GtnSearchResult._first_unit_price_rect[3]
        )
        self.__gtn_window_screenshot = gtn_window_screenshot
        name_image = self._crop_image(name_rect)
        name_image = screenshot.prepare_image_for_ocr(name_image)
        time_image = self._crop_image(time_rect)
        time_image = screenshot.prepare_image_for_ocr(time_image)
        seller_image = self._crop_image(seller_rect)
        seller_image = screenshot.prepare_image_for_ocr(seller_image)
        unit_price_image = self._crop_image(unit_price_rect)
        unit_price_image = screenshot.prepare_image_for_ocr(unit_price_image)
        name = pytesseract.image_to_string(name_image).strip()
        if GtnSearchResult._lokath in name:
            name = re.sub(GtnSearchResult._lokath, 'Iokath', name)

        self.name = re.sub(r'\s+', ' ', name)
        self.time = pytesseract.image_to_string(time_image).strip()
        seller = pytesseract.image_to_string(seller_image).strip()
        self.seller = re.sub(r'\s+', '', seller)
        unit_price = pytesseract.image_to_string(unit_price_image, config = Window.tesseract_custom_config).strip()
        self.unit_price = int(unit_price.replace(',', ''))

    def _crop_image(self, rect):
        return self.__gtn_window_screenshot[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]].copy()