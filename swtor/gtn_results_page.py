from .window import Window
import swtor.screenshot as screenshot
import cv2
import numpy
import os
import swtor.global_data as global_data
import pytesseract
from .ocr_error import OcrError
from .gtn_search_result import GtnSearchResult
import swtor.template_match as template_match

class GtnResultsPage():
    def __init__(self, gtn_window):
        self.__buy_item_template = cv2.imread(os.path.join(Window.template_base_path, 'Buy Item.png'), cv2.IMREAD_GRAYSCALE)
        self.__gtn_window = gtn_window
        self.__result_count = None

    @property
    def result_count(self):
        if not self.__result_count:
            buy_item_locations = template_match.match_template_to_image_multiple_occurrences(screenshot.take_game_window_partial_screenshot(self.__gtn_window.rect), self.__buy_item_template)
            z = numpy.array(list(zip(*buy_item_locations[::-1])))
            self.__result_count = len(z)

        return self.__result_count

    @property
    def __first_item_price_location(self):
        self._wait_for_visible()
        window_location = numpy.array(self.location)
        return window_location + numpy.array(self.__first_item_price_offset)

    def lowest_price(self, item_name):
        if self.__gtn_window.has_results:
            result_count = self.result_count
            for result_index in range(result_count):
                result = GtnSearchResult(self.__gtn_window, result_index)
                if result.name == item_name:
                    return result.unit_price

        return None

    def results(self, item_name):
        if self.__gtn_window.has_results:
            result_count = self.result_count
            results = None
            gtn_window_screenshot = screenshot.take_game_window_partial_screenshot(self.__gtn_window.rect)
            for result_index in range(result_count):
                result = GtnSearchResult(gtn_window_screenshot, result_index)
                if result.name == item_name:
                    if results is None:
                        results = []

                    results.append(result)

            return results

        return None

    # def save_first_item_price_image_processed(self):
    #     first_item_price_location = self.__first_item_price_location
    #     first_item_price_rect = (
    #         first_item_price_location[0],
    #         first_item_price_location[1],
    #         self.__first_item_price_size[0],
    #         self.__first_item_price_size[1]
    #     )
    #     image = take_game_window_partial_screenshot(first_item_price_rect)
    #     image_with_border = cv2.copyMakeBorder(image, 20, 20, 20, 0, cv2.BORDER_REPLICATE)
    #     image_with_border_and_threshold = cv2.threshold(image_with_border, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #     price_string = pytesseract.image_to_string(image_with_border_and_threshold, config = Window.tesseract_custom_config).strip()
    #     cv2.imwrite(os.path.join('training1', f'{price_string}.png'), image_with_border_and_threshold)

    # def save_all_item_price_images_on_page_processed(self):
    #     first_item_price_location = self.__first_item_price_location
    #     for num_offsets in range(self.__results_per_page):
    #         item_price_rect = (
    #             first_item_price_location[0],
    #             first_item_price_location[1] + (num_offsets * self.__result_height),
    #             self.__first_item_price_size[0],
    #             self.__first_item_price_size[1]
    #         )
    #         image = take_game_window_partial_screenshot(item_price_rect)
    #         image_with_border = cv2.copyMakeBorder(image, 20, 20, 20, 0, cv2.BORDER_REPLICATE)
    #         image_with_border_and_threshold = cv2.threshold(image_with_border, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #         price_string = pytesseract.image_to_string(image_with_border_and_threshold, config = Window.tesseract_custom_config).strip()
    #         counter = 1
    #         directory = 'training-processed'
    #         file_name = os.path.join(directory, f'{price_string}.png')
    #         while os.path.exists(file_name):
    #             counter += 1
    #             file_name = os.path.join(directory, f'{price_string}-{counter}.png')
    #         cv2.imwrite(file_name, image_with_border_and_threshold)

    # def save_all_item_price_images_on_page_raw(self, item_price_index):
    #     first_item_price_location = self.__first_item_price_location
    #     for num_offsets in range(self.__results_per_page):
    #         if item_price_index > -1 and not num_offsets == item_price_index - 1:
    #             continue

    #         item_price_rect = (
    #             first_item_price_location[0],
    #             first_item_price_location[1] + (num_offsets * self.__result_height),
    #             self.__first_item_price_size[0],
    #             self.__first_item_price_size[1]
    #         )
    #         image = take_game_window_partial_screenshot_color(item_price_rect)
    #         price_string = pytesseract.image_to_string(image, config = Window.tesseract_custom_config).strip()
    #         counter = 1
    #         directory = 'training-raw'
    #         file_name = os.path.join(directory, f'{price_string}.png')
    #         while os.path.exists(file_name):
    #             counter += 1
    #             file_name = os.path.join(directory, f'{price_string}-{counter}.png')
    #         cv2.imwrite(file_name, image)

    # def save_all_item_price_images_on_page_raw_single_image(self):
    #     print(self.location)
    #     first_overall_price_location = self.location + numpy.array([760, 85])
    #     all_prices_rect = (
    #         first_overall_price_location[0],
    #         first_overall_price_location[1],
    #         232,
    #         470
    #     )
    #     image = take_game_window_partial_screenshot_color(all_prices_rect)
    #     cv2.imwrite(os.path.join('training4', f'{str(uuid.uuid4())}.png'), image)
    #     # first_item_price_location = self.__first_item_price_location
    #     # for num_offsets in range(self.__results_per_page):
    #     #     item_price_rect = (
    #     #         first_item_price_location[0],
    #     #         first_item_price_location[1] + (num_offsets * self.__result_height),
    #     #         self.__first_item_price_size[0],
    #     #         self.__first_item_price_size[1]
    #     #     )
    #     #     image = take_game_window_partial_screenshot_color(item_price_rect)
    #     #     cv2.imwrite(os.path.join('training3', f'{str(uuid.uuid4())}.png'), image)