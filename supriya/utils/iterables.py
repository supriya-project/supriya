import itertools
from typing import (
    Dict,
    Generator,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

T = TypeVar("T")
IT = Iterable[Union[T, "IT"]]


class Expander(Generic[T]):
    def __call__(
        self,
        mapping: Dict[str, Union[T, Sequence[T]]],
        unexpanded: Optional[Iterable[str]] = None,
        only: Optional[Iterable[str]] = None,
    ) -> List[Dict[str, Union[T, Sequence[T]]]]:
        only_ = set(only or ())
        unexpanded_ = set(unexpanded or ())
        expanded_mappings = []
        maximum_length = 1
        massaged: Dict[str, Sequence[T]] = {}
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
            expanded_mapping: Dict[str, Union[T, Sequence[T]]] = {}
            for key, value in massaged.items():
                if key in unexpanded_:
                    expanded_mapping[key] = value
                else:
                    expanded_mapping[key] = value[i % len(value)]
            expanded_mappings.append(expanded_mapping)
        return expanded_mappings


def expand(
    mapping: Dict[str, Union[T, Sequence[T]]],
    unexpanded: Optional[Iterable[str]] = None,
    only: Optional[Iterable[str]] = None,
) -> List[Dict[str, Union[T, Sequence[T]]]]:
    return Expander[T]()(mapping, unexpanded, only)


def flatten(
    iterable: IT, terminal_types: Optional[Union[Type, Tuple[Type, ...]]] = None
) -> Generator[T, None, None]:
    for x in iterable:
        if isinstance(x, Iterable) and (
            terminal_types is None or not isinstance(x, terminal_types)
        ):
            yield from flatten(x, terminal_types)
        else:
            yield x


def group_by_count(iterable: Iterable[T], count: int) -> Generator[List[T], None, None]:
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
    temp: List[Iterable[T]] = []
    for idx, it in enumerate(iterables):
        it = itertools.islice(it, idx, None)
        temp.append(it)
    yield from zip(*temp)


def repeat_to_length(iterable: Iterable[T], length: int) -> Generator[T, None, None]:
    for i, x in enumerate(itertools.cycle(iterable)):
        if i >= length:
            break
        yield x


def zip_cycled(*args: Iterable[T]) -> Generator[Iterable[T], None, None]:
    maximum_i = max(len(_) for _ in args) - 1
    cycles = [itertools.cycle(_) for _ in args]
    iterator = enumerate(zip(*cycles))
    for i, result in iterator:
        yield result
        if i == maximum_i:
            break
