from typing import List
import time
from src.asserts import is_iterable_not_str_predicate


def flat_inner(item):
    res = []
    if is_iterable_not_str_predicate(item):
        for sub in item:
            flatted_item = flat_inner(sub)
            if is_iterable_not_str_predicate(flatted_item):
                res.extend(flatted_item)
            else:
                res.append(flatted_item)
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
