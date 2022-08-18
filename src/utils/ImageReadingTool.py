import os
from typing import Tuple, List
import cv2 as cv
from numpy import ndarray, fromfile, uint8


def read_img_from_dir(dirname: str) -> Tuple[List[ndarray], List[str]]:
    img_list = []
    filepath_list = []
    for filename in os.listdir(dirname):
        path = os.path.join(dirname, filename)
        img = cv.imdecode(fromfile(path, dtype=uint8), -1)
        img_list.append(img)
        filepath_list.append(path)
    return img_list, filepath_list
