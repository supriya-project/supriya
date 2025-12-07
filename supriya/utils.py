"""
Utility functions.
"""

import contextlib
import cProfile
import itertools
import pstats
from typing import (
    Generator,
    Generic,
    Iterable,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

T = TypeVar("T")
IT = Iterable[Union[T, "IT"]]
LT = list[Union[T, "LT"]]


class Expander(Generic[T]):
    def __call__(
        self,
        mapping: dict[str, Union[T, Sequence[T]]],
        unexpanded: Iterable[str] | None = None,
        only: Iterable[str] | None = None,
    ) -> list[dict[str, Union[T, Sequence[T]]]]:
        only_ = set(only or ())
        unexpanded_ = set(unexpanded or ())
        expanded_mappings = []
        maximum_length = 1
        massaged: dict[str, Sequence[T]] = {}
        for key, value in mapping.items():
            if only_ and key not in only_:
                continue
            if isinstance(value, Sequence):
                if key not in unexpanded_:
                    maximum_length = max(len(value), maximum_length)
            else:
                value = [value]
            massaged[key] = value
        for i in range(maximum_length):
            expanded_mapping: dict[str, Union[T, Sequence[T]]] = {}
            for key, value in massaged.items():
                if key in unexpanded_:
                    expanded_mapping[key] = value
                else:
                    expanded_mapping[key] = value[i % len(value)]
            expanded_mappings.append(expanded_mapping)
        return expanded_mappings


def expand(
    mapping: dict[str, Union[T, Sequence[T]]],
    unexpanded: Iterable[str] | None = None,
    only: Iterable[str] | None = None,
) -> list[dict[str, Union[T, Sequence[T]]]]:
    return Expander[T]()(mapping, unexpanded, only)


def expand_deep(item: list[LT]) -> list[list[LT]]:
    size = 1
    for x in item:
        if isinstance(x, Sequence):
            size = max(len(x), size)
    should_recurse = False
    sequences: list[list[LT]] = [[] for _ in range(size)]
    assert len(sequences) == size
    for x in item:
        for i in range(size):
            v: LT
            if isinstance(x, Sequence):
                v = x[i % len(x)]
                if isinstance(v, Sequence):
                    if len(v) > 1:
                        should_recurse = True
                    else:
                        v = v[0]
            else:
                v = x
            sequences[i].append(v)
    if should_recurse:
        for j in reversed(range(size)):
            sequences[j : j + 1] = expand_deep(sequences[j])
    for sequence in sequences:
        assert all(not isinstance(x, Sequence) for x in sequence)
    return sequences


def flatten(
    iterable: IT, terminal_types: Type | tuple[Type, ...] | None = None
) -> Generator[T, None, None]:
    for x in iterable:
        if terminal_types and isinstance(x, terminal_types):
            yield cast(T, x)
        elif isinstance(x, Iterable):
            yield from flatten(x, terminal_types)
        else:
            yield x


def group_by_count(iterable: Iterable[T], count: int) -> Generator[list[T], None, None]:
    iterator = iter(iterable)
    while True:
        group = list(itertools.islice(iterator, count))
        if not group:
            return
        yield group


def iterate_nwise(
    iterable: Iterable[T], n: int = 2
) -> Generator[Sequence[T], None, None]:
    iterables = itertools.tee(iterable, n)
    temp: list[Iterable[T]] = []
    for idx, it in enumerate(iterables):
        it = itertools.islice(it, idx, None)
        temp.append(it)
    yield from zip(*temp)


def repeat_to_length(iterable: Iterable[T], length: int) -> Generator[T, None, None]:
    for i, x in enumerate(itertools.cycle(iterable)):
        if i >= length:
            break
        yield x


def zip_cycled(*args: Sequence[T]) -> Generator[Sequence[T], None, None]:
    maximum_i = max(len(_) for _ in args) - 1
    cycles = [itertools.cycle(_) for _ in args]
    iterator = enumerate(zip(*cycles))
    for i, result in iterator:
        yield result
        if i == maximum_i:
            break


@contextlib.contextmanager
def profile() -> Generator[None, None, None]:
    with cProfile.Profile() as profiler:
        yield
    pstats.Stats(profiler).sort_stats("cumulative").print_stats()
