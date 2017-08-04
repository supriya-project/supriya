import collections


def flatten_iterable(iterable):
    for x in iterable:
        if isinstance(x, collections.Iterable):
            yield from flatten_iterable(x)
        else:
            yield x
