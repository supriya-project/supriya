import pytest

from supriya.patterns import RandomPattern


@pytest.mark.parametrize(
    "minimum, maximum, iterations, is_infinite",
    [
        (0.0, 1.0, None, True),
        (0.0, 1.0, 1, False),
        (0.45, 0.55, None, True),
        (0.0, (1.0, 2.0), None, True),
    ],
)
def test(minimum, maximum, iterations, is_infinite):
    pattern = RandomPattern(minimum=minimum, maximum=maximum, iterations=iterations)
    assert pattern.distribution == RandomPattern.Distribution.WHITE_NOISE
    assert pattern.is_infinite == is_infinite
    assert pattern.iterations == iterations
    assert pattern.maximum == maximum
    assert pattern.minimum == minimum
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
    else:
        assert len(actual) == iterations
    # TODO: Verify minimum / maximum bounds
    assert len(set(actual)) == len(actual)
