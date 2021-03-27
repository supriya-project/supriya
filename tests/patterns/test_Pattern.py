import operator

import pytest

from supriya.patterns import BinaryOpPattern, SequencePattern, UnaryOpPattern


@pytest.mark.parametrize(
    "op, expr_one, expr_two, expected",
    [
        (
            operator.add,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern("+", 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.add,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern("+", SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.floordiv,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern("//", 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.floordiv,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern("//", SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.mod,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern("%", 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.mod,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern("%", SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.mul,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern("*", 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.mul,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern("*", SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.pow,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern("**", 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.pow,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern("**", SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.sub,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern("-", 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.sub,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern("-", SequencePattern([1, 2, 3]), 23),
        ),
        (
            operator.truediv,
            23,
            SequencePattern([1, 2, 3]),
            BinaryOpPattern("/", 23, SequencePattern([1, 2, 3])),
        ),
        (
            operator.truediv,
            SequencePattern([1, 2, 3]),
            23,
            BinaryOpPattern("/", SequencePattern([1, 2, 3]), 23),
        ),
    ],
)
def test_binary_ops(op, expr_one, expr_two, expected):
    if isinstance(expected, Exception):
        with pytest.raises(expected):
            op(expr_one, expr_two)
    else:
        assert op(expr_one, expr_two) == expected


@pytest.mark.parametrize(
    "op, expr, expected",
    [
        (
            operator.abs,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern("abs", SequencePattern([1, 2, 3])),
        ),
        (
            operator.inv,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern("~", SequencePattern([1, 2, 3])),
        ),
        (
            operator.neg,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern("-", SequencePattern([1, 2, 3])),
        ),
        (
            operator.pos,
            SequencePattern([1, 2, 3]),
            UnaryOpPattern("+", SequencePattern([1, 2, 3])),
        ),
    ],
)
def test_unary_ops(op, expr, expected):
    if isinstance(expected, Exception):
        with pytest.raises(expected):
            op(expr)
    else:
        assert op(expr) == expected
