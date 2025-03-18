import operator
from typing import Callable

import pytest

from supriya.patterns import BinaryOpPattern, Pattern, SequencePattern, UnaryOpPattern


@pytest.mark.parametrize(
    "op, expr_one, expr_two, expected",
    [
        (
            operator.add,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.add, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.add,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.add, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.and_,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.and_, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.and_,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.and_, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.floordiv,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.floordiv, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.floordiv,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.floordiv, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.ge,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.le, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.ge,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.ge, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.gt,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.lt, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.gt,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.gt, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.le,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.ge, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.le,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.le, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.lshift,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.lshift, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.lshift,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.lshift, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.lt,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.gt, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.lt,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.lt, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.mod,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.mod, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.mod,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.mod, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.mul,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.mul, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.mul,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.mul, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.or_,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.or_, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.or_,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.or_, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.pow,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.pow, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.pow,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.pow, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.rshift,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.rshift, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.rshift,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.rshift, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.sub,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.sub, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.sub,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.sub, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.truediv,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.truediv, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.truediv,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.truediv, SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.xor,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern(operator.xor, 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.xor,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern(operator.xor, SequencePattern([1, 2, 3]), 23),
        ),
    ],
)
def test_binary_ops(
    op: Callable,
    expr_one: Pattern | float,
    expr_two: Pattern | float,
    expected: Pattern,
) -> None:
    assert op(expr_one, expr_two) == expected


@pytest.mark.parametrize(
    "op, expr, expected",
    [
        (
            operator.abs,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern[int](operator.abs, SequencePattern([1, 2, 3])),
        ),
        (
            operator.inv,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern[int](operator.invert, SequencePattern([1, 2, 3])),
        ),
        (
            operator.neg,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern[int](operator.neg, SequencePattern([1, 2, 3])),
        ),
        (
            operator.pos,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern[int](operator.pos, SequencePattern([1, 2, 3])),
        ),
    ],
)
def test_unary_ops(op: Callable, expr: Pattern, expected: Pattern) -> None:
    assert op(expr) == expected
