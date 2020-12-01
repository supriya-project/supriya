"""
Utility functions.

These will be migrated out into a base package at some point.
"""

import importlib
import itertools
import pathlib
from collections.abc import Iterable


def locate(path: str) -> pathlib.Path:
    if ":" in path:
        module_path, _, file_path = path.partition(":")
        module = importlib.import_module(module_path)
        if hasattr(module, "__file__"):
            return pathlib.Path(module.__file__).parent / file_path
        return pathlib.Path(module.__path__[0]) / file_path  # type: ignore
    return pathlib.Path(path)


def flatten_iterable(iterable):
    for x in iterable:
        if isinstance(x, Iterable):
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
