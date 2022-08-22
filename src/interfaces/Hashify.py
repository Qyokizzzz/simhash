from abc import ABCMeta, abstractmethod
from typing import Optional, Union


class Hashify(metaclass=ABCMeta):

    @abstractmethod
    def hashify(self, word: Optional[Union[str, int]]) -> str:
        """
        hashify(word) -> str

            A customizable callback function to specify the hash algorithm.

            Parameters
            ----------
            word : str or int
                word or image hist index

            Returns
            -------
            out : str
                A string of hashed word
        """
        pass
