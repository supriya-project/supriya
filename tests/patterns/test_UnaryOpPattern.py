import pytest

from supriya.patterns import SequencePattern, UnaryOpPattern
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, operator, input_, expected, is_infinite",
    [
        (None, "-", 1, [-1], True),
        (None, "-", [1], [(-1,)], True),
        (None, "-", [[1]], [((-1,),)], True),
        (None, "-", [[[1]]], [(((-1,),),)], True),
        (None, "-", [1, 2], [(-1, -2)], True),
        (None, "-", SequencePattern([1, 2, 3]), [-1, -2, -3], False),
        (None, "-", SequencePattern([1, 2, 3], None), [-1, -2, -3], True),
    ],
)
def test(stop_at, operator, input_, expected, is_infinite):
    pattern = UnaryOpPattern(operator, input_)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
