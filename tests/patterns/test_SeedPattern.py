import pytest

from supriya.patterns import ChoicePattern, SeedPattern, SequencePattern
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, pattern, expected, is_infinite",
    [
        (None, SequencePattern([1, 2, 3, 4]), [1, 2, 3, 4], False),
        (1, SequencePattern([1, 2, 3, 4]), [1], False),
    ],
)
def test(stop_at, pattern, expected, is_infinite):
    pattern = SeedPattern(pattern)
    run_pattern_test(pattern, expected, is_infinite, stop_at)


def test_random():
    pattern = ChoicePattern([1, 2, 3])
    assert len(set(tuple(pattern) for _ in range(10))) > 1
    pattern = SeedPattern(ChoicePattern([1, 2, 3]))
    assert len(set(tuple(pattern) for _ in range(10))) == 1
