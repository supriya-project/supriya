import operator
from typing import Callable, Sequence, TypeAlias

import pytest

from supriya.patterns import Pattern, SequencePattern, UnaryOpPattern
from supriya.patterns.testutils import run_pattern_test

PatternInput: TypeAlias = int | Sequence["PatternInput"]


@pytest.mark.parametrize(
    "stop_at, operator, input_, expected, is_infinite",
    [
        (None, operator.neg, 1, [-1], True),
        (None, operator.neg, [1], [(-1,)], True),
        (None, operator.neg, [[1]], [((-1,),)], True),
        (None, operator.neg, [[[1]]], [(((-1,),),)], True),
        (None, operator.neg, [1, 2], [(-1, -2)], True),
        (None, operator.neg, SequencePattern([1, 2, 3]), [-1, -2, -3], False),
        (None, operator.neg, SequencePattern([1, 2, 3], None), [-1, -2, -3], True),
    ],
)
def test_pattern(
    stop_at: float | None,
    operator: Callable,
    input_: Pattern | PatternInput,
    expected: PatternInput,
    is_infinite: bool,
) -> None:
    pattern = UnaryOpPattern(operator, input_)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
