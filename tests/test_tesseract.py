import glob
import cv2
from pathlib import Path
import pytesseract
import pytest
import os

def unchanged(image_path):
    return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

def color(image_path):
    return cv2.imread(image_path, cv2.IMREAD_COLOR)

def gray(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('gray.png', image)
    return image

def gray_border_const(image_path):
    image = gray(image_path)
    return cv2.copyMakeBorder(image, 20, 20, 20, 0, cv2.BORDER_CONSTANT, 0)

def color_border_const(image_path):
    image = color(image_path)
    return cv2.copyMakeBorder(image, 20, 20, 20, 0, cv2.BORDER_CONSTANT, 0)

def gray_border_rep(image_path):
    image = gray(image_path)
    return cv2.copyMakeBorder(image, 4, 4, 4, 0, cv2.BORDER_REPLICATE)

def color_border_rep(image_path):
    image = color(image_path)
    return cv2.copyMakeBorder(image, 20, 20, 20, 0, cv2.BORDER_REPLICATE)

def otsu(image_path):
    image = upscale_2x(image_path)
    image_otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite('otsu.png', image_otsu)
    return image_otsu

def otsu_border(image_path):
    image = gray_border_rep(image_path)
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

def upscale_2x(image_path):
    image = gray(image_path)
    upscaled = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2), interpolation = cv2.INTER_AREA)
    cv2.imwrite('upscale_2x.png', upscaled)
    return upscaled

@pytest.fixture(params = [otsu, otsu_border])
def image_loaders(request):
    return request.param

@pytest.fixture(params = glob.glob('training2/*.png'), ids = [Path(p).stem for p in glob.glob('training2/*.png')])
def image_paths(request):
    return request.param

@pytest.fixture(params = [8]) #, 9, 13])
def psms(request):
    return f'--psm {str(request.param)}'

@pytest.fixture(params = [1]) #, 3])
def oems(request):
    return f'--oem {str(request.param)}'

# def test_training_data(image_paths, image_loaders, psms, oems):
#     image = image_loaders(image_paths)
#     string = pytesseract.image_to_string(image, config = f'-c tessedit_char_whitelist=",0123456789" {psms} {oems}').strip()
#     assert Path(image_paths).stem.strip() == string

# @pytest.mark.parametrize("image_path", glob.glob('training2/*.png'))
# def test_training_data_color(image_path):
#     image = gray(image_path)
#     string = pytesseract.image_to_string(image, config = r'-c tessedit_char_whitelist=",0123456789" --psm 6 --oem 3').strip()
#     assert Path(image_path).stem.strip() == string

@pytest.fixture(params = glob.glob('training1/*.png'), ids = [Path(p).stem for p in glob.glob('training1/*.png')])
def image_paths_x(request):
    return request.param

def test_training_data(image_paths_x):
    image = cv2.imread(image_paths_x, cv2.IMREAD_GRAYSCALE)
    upscaled = cv2.resize(image, (image.shape[1] * 10, image.shape[0] * 10), interpolation = cv2.INTER_AREA)
    string = pytesseract.image_to_string(upscaled, config = r'-c tessedit_char_whitelist=",0123456789" --psm 6 --oem 3').strip()
    assert Path(image_paths_x).stem.strip() == string