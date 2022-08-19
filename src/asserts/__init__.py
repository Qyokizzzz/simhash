from typing import Sequence


def equal_length_assert(seq1: Sequence, seq2: Sequence):
    if len(seq1) != len(seq2):
        raise Exception('The lengths of %s and %s must be equal.' % (seq1, seq2))
