import os
import cv2
import mss
import numpy
from matplotlib import pyplot as plt

methods_path = 'methods'

def try_all_methods_gray():
    with mss.mss() as sct:
        swtor_screenshot_img = sct.grab(sct.monitors[2])
    swtor_screenshot_data = numpy.array(swtor_screenshot_img)
    swtor_screenshot_data_gray = cv2.cvtColor(swtor_screenshot_data, cv2.COLOR_BGRA2GRAY)
    options_window_data = cv2.imread('ui-templates/Options.png', 0)
    w, h = options_window_data.shape[::-1]
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = swtor_screenshot_data_gray.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img, options_window_data, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(meth)
        print(cv2.minMaxLoc(res))

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()

def try_all_methods_color(template_name: str, experiment_name: str):
    with mss.mss() as sct:
        swtor_screenshot_img = sct.grab(sct.monitors[2])
    swtor_screenshot_data = numpy.array(swtor_screenshot_img)
    # cv2.imwrite(os.path.join(methods_path, experiment_name, 'swtor_screenshot_data.png'), swtor_screenshot_data)
    # swtor_screenshot_data_color = numpy.flip(swtor_screenshot_data[:, :, :3], 2)
    swtor_screenshot_data_color = cv2.cvtColor(swtor_screenshot_data, cv2.COLOR_BGRA2GRAY)
    # cv2.imwrite(os.path.join(methods_path, experiment_name, 'swtor_screenshot_data_color.png'), swtor_screenshot_data_color)
    # options_window_data = cv2.imread(os.path.join('ui-templates', f'{template_name}.png'), cv2.IMREAD_COLOR)
    options_window_data = cv2.imread(os.path.join('ui-templates', f'{template_name}.png'), cv2.IMREAD_GRAYSCALE)
    # cv2.imwrite(os.path.join(methods_path, experiment_name, 'window_data.png'), options_window_data)
    # w = options_window_data.shape[1]
    # h = options_window_data.shape[0]
    w, h = options_window_data.shape[::-1]
    # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    methods = ['cv2.TM_CCOEFF_NORMED']

    results_path = os.path.join(methods_path, experiment_name, 'results.txt')
    if not os.path.exists(os.path.dirname(results_path)):
        os.makedirs(os.path.dirname(results_path))

    with open(results_path, 'w') as results_file:
        for meth in methods:
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(swtor_screenshot_data_color, options_window_data, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            threshold = 0.95
            locations = numpy.where(res >= threshold)
            # print(len(locations[0]))
            # print(len(locations[1]))
            z = numpy.array(list(zip(*locations[::-1])))
            ind = numpy.lexsort((z[:,0],z[:,1]))
            print(z[ind][0])

            results_file.write(meth)
            results_file.write('\n')
            results_file.write(str(cv2.minMaxLoc(res)))
            results_file.write('\n')

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            # img = swtor_screenshot_data.copy()
            img = swtor_screenshot_data_color.copy()
            cv2.rectangle(img,top_left, bottom_right, 255, 2)

            # plt.subplot(121),plt.imshow(res,cmap = 'gray')
            # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            # plt.subplot(122),plt.imshow(img,cmap = 'gray')
            # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            # plt.suptitle(meth)

            # plt.show()
            # plt.savefig(os.path.join(methods_path, experiment_name, f'{meth}.png'))
            cv2.imwrite(os.path.join(methods_path, experiment_name, f'{meth}.png'), img)