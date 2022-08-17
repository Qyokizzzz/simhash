from abc import ABCMeta, abstractmethod
from typing import Optional, Union, List
from numpy import ndarray


class CharacteristicIdxListExtractor(metaclass=ABCMeta):
    @abstractmethod
    def get_characteristic_idx_list(
        self,
        imhist: Optional[Union[List[int], ndarray]],
        com_hists: List[List[int]]
    ) -> List[int]:
        pass
