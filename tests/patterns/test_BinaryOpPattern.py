import pytest

from supriya.patterns import BinaryOpPattern, SequencePattern
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, operator, input_a, input_b, expected, is_infinite",
    [
        (None, "+", 1, 7, [8], True),
        (None, "+", [1], 7, [(8,)], True),
        (None, "+", [1], [7], [(8,)], True),
        (None, "+", [[1]], [7], [((8,),)], True),
        (None, "+", [[[1]]], [7], [(((8,),),)], True),
        (None, "+", [1, 2], [7, 8], [(8, 10)], True),
        (None, "+", [1, 2], [7, 8, 10], [(8, 10, 11)], True),
        (None, "*", SequencePattern([1, 2, 3]), 4, [4, 8, 12], False),
        (None, "*", SequencePattern([1, 2, 3], None), 4, [4, 8, 12], True),
    ],
)
def test(stop_at, operator, input_a, input_b, expected, is_infinite):
    pattern = BinaryOpPattern(operator, input_a, input_b)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
