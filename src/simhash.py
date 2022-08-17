from typing import Optional, Union, List, Callable
from numpy import zeros, array, ndarray


class Simhash(object):
    def __init__(self, hashify: Callable, n: int = 128) -> None:
        if hashify is None:
            raise Exception('hashify is required argument')
        self.hashify = hashify
        self.n = n

    def generate(self, characteristic_idx_list: List[int]) -> str:
        characteristic_hash_list = list(map(
            self.hashify,
            characteristic_idx_list
        ))
        weights = self._gen_weights(characteristic_hash_list)
        return ''.join(map(
            lambda x: '1' if x > 0 else '0',
            weights
        ))

    def _gen_weights(self, characteristic_hash_list: Optional[Union[map, List[str]]]) -> ndarray:
        res = zeros(self.n, dtype=int)

        for ch in characteristic_hash_list:
            tmp = list(map(lambda x: 1 if x == '1' else -1, ch))
            if len(tmp) < self.n:
                # 首位为0时会少位，因此首位补零
                fill = [0 for _ in range(self.n - len(tmp))]
                fill.extend(tmp)
                tmp = fill
            res += array(tmp, dtype=int)

        return res

    @staticmethod
    def calc_hamming_dist(simhash1: str, simhash2: str) -> int:
        if len(simhash1) != len(simhash2):
            raise Exception('The length of input sequences must be same.')
        return bin(int(simhash1, 2) ^ int(simhash2, 2)).count('1')

    @staticmethod
    def segment(simhash: str, n: int) -> List[str]:
        total_length = len(simhash)
        if total_length % n != 0:
            raise Exception('The number of bits in the simhash must be divisible by n.')
        segmented_simhash = []
        sub_length = int(total_length / n)
        start = 0
        end = sub_length
        for _ in range(n):
            segmented_simhash.append(simhash[start: end])
            start += sub_length
            end += sub_length

        return segmented_simhash
