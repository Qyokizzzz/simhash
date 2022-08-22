from typing import Sequence, Any
from collections.abc import Iterable


def is_iterable_not_str_predicate(item: Any) -> bool:
    return isinstance(item, Iterable) and not isinstance(item, str)


def equal_length_assert(seq1: Sequence, seq2: Sequence):
    if len(seq1) != len(seq2):
        raise Exception('The lengths of %s and %s must be equal.' % (seq1, seq2))


def not_empty_assert(doc: Any):
    if not doc:
        raise Exception('Cannot entering an empty document.')
