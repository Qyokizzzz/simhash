import os
from random import random, randint, uniform
from typing import Optional, Union, Tuple, List, Callable
from numpy import ndarray, fromfile, uint8
import cv2 as cv


class ComHistsGetter:
    def __init__(self, extractor: Callable):
        self.extractor = extractor

    @staticmethod
    def _get_slice(h: int, w: int, n: int, scale: float) -> Tuple[slice, slice]:
        if h <= w:
            window_size = randint(int(h * scale / 2), int(h * scale * 2))
        else:
            window_size = randint(int(w * scale / 2), int(w * scale * 2))

        starts = {
            1: (slice(0, window_size), slice(0, window_size)),
            2: (slice(0, window_size), slice(-window_size, -1)),
            3: (slice(-window_size, -1), slice(0, window_size)),
            4: (slice(-window_size, -1), slice(-window_size, -1)),
            5: (
                slice(
                    randint(int(h / 2 - h / 2 * scale), int(h / 2)),
                    randint(int(h / 2) + 1, int(h / 2 + h / 2 * scale))
                ),
                slice(
                    randint(int(w / 2 - w / 2 * scale), int(w / 2)),
                    randint(int(w / 2)+1, int(w / 2 + w / 2 * scale))
                )
            )
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
                ordinary_hist = self.extractor(img[self._get_slice(h, w, randint(1, 4), uniform(0.01, 0.02))])
                random_hist = self.extractor(img[self._get_slice(h, w, 5, uniform(0.01, 0.02))])
                common.append(ordinary_hist + random_hist)
        return common
