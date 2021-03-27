import pytest

from supriya.patterns.events import NullEvent


@pytest.mark.parametrize(
    "event, offset, expected",
    [(NullEvent(), 0.0, []), (NullEvent(delta=1.5), 0.0, []), (NullEvent(), 2.5, [])],
)
def test_expand(event, offset, expected):
    actual = event.expand(offset)
    assert actual == expected
