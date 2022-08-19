import os
from typing import Tuple, List
import cv2 as cv
from numpy import ndarray, fromfile, uint8


def read_img_from_dir(dirname: str) -> Tuple[List[str], List[ndarray]]:
    filepath_list = []
    img_list = []
    for filename in os.listdir(dirname):
        path = os.path.join(dirname, filename)
        img = cv.imdecode(fromfile(path, dtype=uint8), -1)
        filepath_list.append(path)
        img_list.append(img)
    return filepath_list, img_list
