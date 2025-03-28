from typing import Generator, Iterator, Sequence, Union

from uqbar.enums import IntEnumeration

from ..typing import UUIDDict
from .patterns import Pattern, SequencePattern, T


class ChoicePattern(SequencePattern[T]):
    def __init__(
        self,
        sequence: Sequence[Union[T, Pattern[T]]],
        iterations: int | None = 1,
        forbid_repetitions: bool = False,
        weights: Sequence[float] | None = None,
    ) -> None:
        super().__init__(sequence, iterations=iterations)
        self._forbid_repetitions = bool(forbid_repetitions)
        self._weights = tuple(abs(float(x)) for x in weights) if weights else None

    def _iterate(self, state: UUIDDict | None = None) -> Generator[T, bool, None]:
        should_stop = False
        rng = self._get_rng()
        previous_index: int | None = None
        for _ in self._loop(self._iterations):
            if self._weights:
                index = self._find_index_weighted(rng, self._weights)
                while self.forbid_repetitions and index == previous_index:
                    index = self._find_index_weighted(rng, self._weights)
            else:
                index = self._find_index_unweighted(rng)
                while self.forbid_repetitions and index == previous_index:
                    index = self._find_index_unweighted(rng)
            previous_index = index
            choice = self._sequence[index]
            if isinstance(choice, Pattern):
                # MyPy: Function does not return a value (it only ever returns None)
                should_stop = (yield from choice) or should_stop  # type: ignore
            else:
                should_stop = (yield choice) or should_stop
            if should_stop:
                break
        return

    def _find_index_unweighted(self, rng: Iterator[float]) -> int:
        return int(next(rng) * 0x7FFFFFFF) % len(self._sequence)

    def _find_index_weighted(
        self, rng: Iterator[float], weights: Sequence[float]
    ) -> int:
        needle = next(rng) * sum(weights)
        sum_of_weights = 0.0
        for index, weight in enumerate(weights):
            if sum_of_weights <= needle <= sum_of_weights + weight:
                break
            sum_of_weights += weight
        return index

    @property
    def forbid_repetitions(self) -> bool:
        return self._forbid_repetitions

    @property
    def weights(self) -> tuple[float, ...] | None:
        return self._weights


class RandomPattern(Pattern[float]):
    class Distribution(IntEnumeration):
        WHITE_NOISE = 0

    def __init__(
        self,
        minimum: float | Sequence[float] = 0.0,
        maximum: float | Sequence[float] = 1.0,
        iterations: int | None = None,
        distribution: Union["RandomPattern.Distribution", str] = "WHITE_NOISE",
    ) -> None:
        if iterations is not None:
            iterations = int(iterations)
            if iterations < 1:
                raise ValueError("Iterations must be null or greater than 0")
        self._iterations = iterations
        self._distribution: RandomPattern.Distribution = self.Distribution.from_expr(
            distribution
        )
        self._minimum: float = self._freeze_recursive(minimum)
        self._maximum: float = self._freeze_recursive(maximum)

    def _iterate(self, state: UUIDDict | None = None) -> Generator[float, bool, None]:
        def procedure(one: float, two: float) -> float:
            minimum, maximum = sorted([one, two])
            number = next(rng)
            return (number * (maximum - minimum)) + minimum

        rng = self._get_rng()
        for _ in self._loop(self._iterations):
            expr = self._apply_recursive(procedure, self._minimum, self._maximum)
            if (yield expr):
                return

    @property
    def distribution(self) -> Union["RandomPattern.Distribution", str]:
        return self._distribution

    @property
    def is_infinite(self) -> bool:
        return self._iterations is None

    @property
    def iterations(self) -> int | None:
        return self._iterations

    @property
    def minimum(self) -> float:
        return self._minimum

    @property
    def maximum(self) -> float:
        return self._maximum


class ShufflePattern(SequencePattern[T]):
    def __init__(
        self,
        sequence: Sequence[Union[T, Pattern[T]]],
        iterations: int | None = 1,
        forbid_repetitions: bool = False,
    ) -> None:
        super().__init__(sequence, iterations=iterations)
        self._forbid_repetitions = bool(forbid_repetitions)

    def _iterate(self, state: UUIDDict | None = None) -> Generator[T, bool, None]:
        should_stop = False
        rng = self._get_rng()
        previous_index = None
        for _ in self._loop(self._iterations):
            indices = self._shuffle(len(self._sequence), rng)
            while (
                self.forbid_repetitions
                and len(indices) > 1
                and indices[0] == previous_index
            ):
                indices = self._shuffle(len(self._sequence), rng)
            previous_index = indices[-1]
            for index in indices:
                choice = self._sequence[index]
                if isinstance(choice, Pattern):
                    # MyPy: Function does not return a value (it only ever returns None)
                    should_stop = (yield from choice) or should_stop  # type: ignore
                else:
                    should_stop = (yield choice) or should_stop
                if should_stop:
                    return

    def _shuffle(self, length: int, rng: Iterator[float]) -> Sequence[int]:
        indices = list(range(length))
        shuffled_indices = []
        while len(indices) > 1:
            index = int(next(rng) * 0x7FFFFFFF) % len(indices)
            shuffled_indices.append(indices.pop(index))
        if indices:
            shuffled_indices.append(indices.pop())
        return shuffled_indices

    @property
    def forbid_repetitions(self) -> bool:
        return self._forbid_repetitions
