import swtor.global_data as global_data
import cv2
import numpy

def match_template_to_image(image, template):
    template_match_result = cv2.matchTemplate(image, template, eval(global_data.cv2_template_match_method))
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(template_match_result)
    return max_val, max_loc

def match_template_to_image_multiple_occurrences(image, template):
    template_match_result = cv2.matchTemplate(image, template, eval(global_data.cv2_template_match_method))
    locations = numpy.where(template_match_result >= global_data.cv2_template_match_threshold)
    return locations