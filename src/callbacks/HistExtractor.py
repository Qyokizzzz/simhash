from typing import Optional, Union, List
import cv2 as cv
from numpy import ndarray, int32


def hsv_extractor(img: ndarray) -> Optional[Union[ndarray, List[int]]]:
    if len(img.shape) != 3:
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hvs_hist = cv.calcHist(
        [img],
        [0, 1, 2],
        None,
        [16, 4, 4],
        [0, 180, 0, 256, 0, 256]
    ).flatten()
    return hvs_hist.astype(int32)
