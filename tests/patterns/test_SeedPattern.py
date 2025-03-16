import pytest

from supriya.patterns import ChoicePattern, Pattern, SeedPattern, SequencePattern
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, pattern, expected, is_infinite",
    [
        (None, SequencePattern([1, 2, 3, 4]), [1, 2, 3, 4], False),
        (1, SequencePattern([1, 2, 3, 4]), [1], False),
    ],
)
def test_pattern(
    stop_at: float | None, pattern: Pattern, expected: list[float], is_infinite: bool
) -> None:
    run_pattern_test(SeedPattern(pattern), expected, is_infinite, stop_at)


def test_random() -> None:
    choice_pattern = ChoicePattern([1, 2, 3])
    assert len(set(tuple(choice_pattern) for _ in range(10))) > 1
    seed_pattern = SeedPattern(choice_pattern)
    assert len(set(tuple(seed_pattern) for _ in range(10))) == 1
