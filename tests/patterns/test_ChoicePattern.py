import pytest
from uqbar.iterables import nwise

from supriya.patterns import ChoicePattern, SequencePattern


@pytest.mark.parametrize(
    "sequence, iterations, forbid_repetitions, weights, is_infinite",
    [
        ([1, 2, 3], 1, False, None, False),
        ([1, 2, 3], 1, True, None, False),
        ([1, 2, 3], None, False, None, True),
        ([1, 2, 3], None, True, None, True),
        ([1, 2, 3], None, True, [1, 2, 1], True),
        (
            [SequencePattern(["a", "b"]), SequencePattern(["c", "d"])],
            None,
            False,
            None,
            True,
        ),
    ],
)
def test(sequence, iterations, forbid_repetitions, weights, is_infinite):
    pattern = ChoicePattern(
        sequence,
        iterations=iterations,
        forbid_repetitions=forbid_repetitions,
        weights=weights,
    )
    assert pattern.is_infinite == is_infinite
    iterator = iter(pattern)
    ceased = True
    actual = []
    for _ in range(1000):
        try:
            actual.append(next(iterator))
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
    if forbid_repetitions:
        for a, b in nwise(actual):
            assert a != b
