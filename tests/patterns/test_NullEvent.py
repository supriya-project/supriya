import pytest

from supriya.patterns.events import Event, NullEvent, Priority


@pytest.mark.parametrize(
    "event, offset, expected",
    [(NullEvent(), 0.0, []), (NullEvent(delta=1.5), 0.0, []), (NullEvent(), 2.5, [])],
)
def test_expand(
    event: Event, offset: float, expected: list[tuple[float, Priority, Event]]
) -> None:
    actual = event.expand(offset)
    assert actual == expected
