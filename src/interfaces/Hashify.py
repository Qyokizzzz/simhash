from abc import ABCMeta, abstractmethod
from typing import List


class Hashify(metaclass=ABCMeta):
    @abstractmethod
    def hashify(self, characteristic_idx_list: List[int]) -> List[str]:
        pass
