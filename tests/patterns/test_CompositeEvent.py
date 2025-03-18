import uuid

import pytest

from supriya.patterns.events import (
    CompositeEvent,
    Event,
    NodeFreeEvent,
    NullEvent,
    Priority,
)

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [
        (
            CompositeEvent([NullEvent(delta=0.25), NodeFreeEvent(id_, delta=0.0)]),
            0.0,
            [(0.25, Priority.START, NodeFreeEvent(id_))],
        ),
        (
            CompositeEvent([NullEvent(delta=0.5), NodeFreeEvent(id_, delta=0.0)]),
            2.5,
            [(3.0, Priority.START, NodeFreeEvent(id_))],
        ),
    ],
)
def test_expand(
    event: Event, offset: float, expected: list[tuple[float, Priority, Event]]
) -> None:
    print(event)
    actual = event.expand(offset)
    assert actual == expected
