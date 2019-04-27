"""
Utility functions.

These will be migrated out into a base package at some point.
"""

import collections
import itertools


def flatten_iterable(iterable):
    for x in iterable:
        if isinstance(x, collections.Iterable):
            yield from flatten_iterable(x)
        else:
            yield x


def group_iterable_by_count(iterable, count):
    iterator = iter(iterable)
    while True:
        group = list(itertools.islice(iterator, count))
        if not group:
            return
        yield group


def iterate_nwise(iterable, n=2):
    iterables = itertools.tee(iterable, n)
    temp = []
    for idx, it in enumerate(iterables):
        it = itertools.islice(it, idx, None)
        temp.append(it)
    return zip(*temp)


def repeat_sequence_to_length(sequence, length):
    for i, x in enumerate(itertools.cycle(sequence)):
        if i >= length:
            break
        yield x


def zip_sequences(*args):
    maximum_i = max(len(_) for _ in args) - 1
    cycles = [itertools.cycle(_) for _ in args]
    iterator = enumerate(zip(*cycles))
    for i, result in iterator:
        yield result
        if i == maximum_i:
            break
