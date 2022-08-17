from abc import ABCMeta, abstractmethod
from typing import Optional, Union, List
from numpy import ndarray


class HistExtractor(metaclass=ABCMeta):
    @abstractmethod
    def extract(self, img: ndarray) -> Optional[Union[ndarray, List[int]]]:
        pass
