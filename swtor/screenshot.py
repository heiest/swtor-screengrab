import cv2
import numpy
import mss
from ahk import AHK
import swtor.global_data as global_data
from .screenshot_area_invalid_error import ScreenshotAreaInvalidError

def take_screenshot_gray(mss_monitor_dict):
    screenshot = take_screenshot_bgra(mss_monitor_dict)
    return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)

def take_screenshot_bgra(mss_monitor_dict):
    with mss.mss() as sct:
        screenshot = numpy.array(sct.grab(mss_monitor_dict))

    return screenshot

def take_screenshot_bgr(mss_monitor_dict):
    screenshot = take_screenshot_bgra(mss_monitor_dict)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
    return screenshot

def take_game_window_screenshot():
    ahk = AHK()
    game_window_rect = ahk.win_get(title = global_data.swtor_window_ahk_title).rect
    mss_monitor_dict = rect_to_mss_monitor_dict(game_window_rect)
    return take_screenshot_gray(mss_monitor_dict)

def rect_to_mss_monitor_dict(rect):
    return {
        "top": rect[1],
        "left": rect[0],
        "width": rect[2],
        "height": rect[3],
        "mon": 0
    }

def rect_to_corners(rect):
    rect_top_left = numpy.array((rect[0], rect[1]))
    rect_bottom_right = numpy.array((rect[0] + rect[2], rect[1] + rect[3]))
    return (rect_top_left, rect_bottom_right)

def get_game_window_rect():
    ahk = AHK()
    return ahk.win_get(title = global_data.swtor_window_ahk_title).rect

def get_game_window_corners():
    return rect_to_corners(get_game_window_rect())

def corners_contains(outer, inner):
    if (inner[0][0] < outer[0][0] or
        inner[0][1] < outer[0][1] or
        inner[1][0] > outer[1][0] or
        inner[1][1] > outer[1][1]):
            return False

    return True

def game_window_contains_rect(rect):
    game_window_corners = get_game_window_corners()
    adjusted_rect = (
        rect[0] + game_window_corners[0][0],
        rect[1] + game_window_corners[0][1],
        rect[2],
        rect[3])
    rect_corners = rect_to_corners(adjusted_rect)
    return corners_contains(game_window_corners, rect_corners)

def __take_game_window_partial_screenshot(rect, func):
    if not game_window_contains_rect(rect):
        raise ScreenshotAreaInvalidError(rect, AHK().win_get(title = global_data.swtor_window_ahk_title).rect)

    ahk = AHK()
    game_window_rect = ahk.win_get(title = global_data.swtor_window_ahk_title).rect
    game_window_top_left = numpy.array((game_window_rect[0], game_window_rect[1]))
    rect_top_left = numpy.array((rect[0], rect[1]))
    rect_top_left_adjusted = game_window_top_left + rect_top_left
    mss_monitor_dict = rect_to_mss_monitor_dict((rect_top_left_adjusted[0], rect_top_left_adjusted[1], rect[2], rect[3]))
    return func(mss_monitor_dict)

def take_game_window_partial_screenshot(rect):
    return __take_game_window_partial_screenshot(rect, take_screenshot_gray)

def take_game_window_partial_screenshot_color(rect):
    return __take_game_window_partial_screenshot(rect, take_screenshot_bgr)

def take_game_window_partial_screenshot_ocr(rect):
    image = take_game_window_partial_screenshot(rect)
    return prepare_image_for_ocr(image)

def prepare_image_for_ocr(image):
    image = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2), interpolation = cv2.INTER_CUBIC)
    image = cv2.bitwise_not(image)
    return image