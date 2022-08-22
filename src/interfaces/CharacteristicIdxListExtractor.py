from abc import ABCMeta, abstractmethod
from typing import List


class CharacteristicIdxListExtractor(metaclass=ABCMeta):
    @abstractmethod
    def get_characteristic_idx_list(self, *args, **kwargs) -> List[int]:
        pass
