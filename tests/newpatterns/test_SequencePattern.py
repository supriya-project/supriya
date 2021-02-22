import pytest

from supriya.newpatterns import SequencePattern
from supriya.newpatterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, sequence, iterations, expected, is_infinite",
    [
        (None, [1, 2, 3], None, [1, 2, 3], True),
        (None, [1, 2, 3], 1, [1, 2, 3], False),
        (None, [1, 2, 3], 2, [1, 2, 3, 1, 2, 3], False),
        (None, [1, 2, 3, SequencePattern(["a", "b"])], 1, [1, 2, 3, "a", "b"], False),
        (
            None,
            [1, 2, 3, SequencePattern(["a", "b"], None)],
            1,
            [1, 2, 3, "a", "b"],
            True,
        ),
        (
            None,
            [SequencePattern([1, 2, 3]), SequencePattern(["a", "b"])],
            1,
            [1, 2, 3, "a", "b"],
            False,
        ),
        (
            None,
            [SequencePattern([1, 2, 3]), SequencePattern(["a", "b"])],
            2,
            [1, 2, 3, "a", "b", 1, 2, 3, "a", "b"],
            False,
        ),
        (
            None,
            [SequencePattern([1, 2, 3], None), SequencePattern(["a", "b"])],
            1,
            [1, 2, 3],
            True,
        ),
        (
            None,
            [SequencePattern([1, 2, 3], None), SequencePattern(["a", "b"])],
            None,
            [1, 2, 3],
            True,
        ),
    ],
)
def test(stop_at, sequence, iterations, expected, is_infinite):
    pattern = SequencePattern(sequence, iterations=iterations)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
