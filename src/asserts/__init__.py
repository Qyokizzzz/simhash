from typing import List


def equal_length_assert(seq1: List[any], seq2: List[any]):
    if len(seq1) != len(seq2):
        raise Exception('The lengths of %s and %s must be equal.' % (seq1, seq2))
