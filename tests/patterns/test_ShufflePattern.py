import pytest
from uqbar.iterables import group_by_count, nwise

from supriya.patterns import ShufflePattern


@pytest.mark.parametrize(
    "sequence, iterations, forbid_repetitions, stride, is_infinite",
    [
        ([1], 1, False, 1, False),
        ([1], None, False, 1, True),
        ([1, 2, 3], 1, False, 3, False),
        ([1, 2, 3], 2, False, 3, False),
        ([1, 2, 3], None, False, 3, True),
    ],
)
def test(sequence, iterations, forbid_repetitions, stride, is_infinite):
    pattern = ShufflePattern(
        sequence, iterations=iterations, forbid_repetitions=forbid_repetitions
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
    chunks = list(tuple(chunk) for chunk in group_by_count(actual, stride))
    if is_infinite and len(chunks[-1]) != stride:
        chunks.pop()  # If final group is short due to 1000 iterations, discard
    for chunk in chunks:
        assert len(chunk) == len(set(chunk)), chunk
    assert len(set(tuple(sorted(chunk)) for chunk in chunks)) == 1
