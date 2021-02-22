import pytest

from supriya.newpatterns import SeedPattern, SequencePattern
from supriya.newpatterns.testutils import run_pattern_test


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
