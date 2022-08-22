from typing import Optional, Union, List, Callable
from numpy import zeros, array, ndarray
from src.asserts import equal_length_assert


class Simhash(object):
    def __init__(self, hashify: Callable, n_bits: int, hamming_dist_threshold: int) -> None:
        if hashify is None:
            raise Exception('hashify is required argument')
        self.hashify = hashify
        self.n_bits = n_bits
        self.hamming_dist_threshold = hamming_dist_threshold

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
        res = zeros(self.n_bits, dtype=int)

        for ch in characteristic_hash_list:
            tmp = list(map(lambda x: 1 if x == '1' else -1, ch))
            if len(tmp) < self.n_bits:
                # If the first bit is 0, the length of hashify result will be less than n_bits.
                fill = [0 for _ in range(self.n_bits - len(tmp))]
                fill.extend(tmp)
                tmp = fill
            res += array(tmp, dtype=int)

        return res

    @staticmethod
    def calc_hamming_dist(simhash1: str, simhash2: str) -> int:
        equal_length_assert(simhash1, simhash2)
        return bin(int(simhash1, 2) ^ int(simhash2, 2)).count('1')

    def segment(self, simhash: str) -> List[str]:
        total_length = len(simhash)
        if total_length % self.hamming_dist_threshold != 0:
            raise Exception('The number of bits in the simhash must be divisible by n.')
        segmented_simhash = []
        sub_length = int(total_length / self.hamming_dist_threshold)
        start = 0
        end = sub_length
        for _ in range(self.hamming_dist_threshold):
            segmented_simhash.append(simhash[start: end])
            start += sub_length
            end += sub_length

        return segmented_simhash
