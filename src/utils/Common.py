from collections.abc import Iterable
from typing import List
import time


def flat_inner(item):
    res = []
    if isinstance(item, Iterable) and not isinstance(item, str):
        for sub in item:
            res.extend(flat_inner(sub))
        return res
    else:
        return item


def flat(a, b) -> List[any]:
    res = flat_inner(a)
    res.extend(flat_inner(b))
    return res


def timer(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        stop_time = time.time()
        print('The %s function run time is %s second(s)' % (func.__name__, (stop_time - start_time)))
        return res
    return inner
