import os
from math import floor
from random import random, randint, uniform
from typing import Optional, Union, Tuple, List, Callable
from numpy import ndarray, fromfile, uint8
import cv2 as cv


class ComHistsGetter:
    def __init__(self, extractor: Callable):
        self.extractor = extractor

    @staticmethod
    def _get_slice(h: int, w: int, n: int) -> Tuple[slice, slice]:
        if h <= w:
            window_size = randint(int(h * uniform(0, 1) / 2), int(h))
        else:
            window_size = randint(int(w * uniform(0, 1) / 2), int(w))

        rand_start = lambda x: randint(int(x / 2 - x / 2 * uniform(0, 1)), int(x / 2) + 1)
        rand_end = lambda x: randint(int(x / 2) + 1, int(x - floor(x / 2 * uniform(0, 0.99)) + 1))

        starts = {
            1: (slice(0, window_size), slice(0, window_size)),
            2: (slice(0, window_size), slice(-window_size, -1)),
            3: (slice(-window_size, -1), slice(0, window_size)),
            4: (slice(-window_size, -1), slice(-window_size, -1)),
            5: (slice(rand_start(h), rand_end(h)), slice(rand_start(w), rand_end(w)))
        }
        return starts[n]

    def get_common_hist(self, dirname: str, p: float) -> Optional[Union[List[ndarray], List[List[int]]]]:
        common = []
        for filename in os.listdir(dirname):
            if random() <= p:
                img = cv.imdecode(fromfile(os.path.join(dirname, filename), dtype=uint8), -1)
                if len(img.shape) == 3:
                    h, w, _ = img.shape
                else:
                    h, w = img.shape
                ordinary_hist = self.extractor(img[self._get_slice(h, w, randint(1, 4))])
                random_hist = self.extractor(img[self._get_slice(h, w, 5)])
                common.append(ordinary_hist + random_hist)
        return common
