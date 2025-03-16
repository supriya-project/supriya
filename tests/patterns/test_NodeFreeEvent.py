from unittest.mock import Mock, call
from uuid import UUID, uuid4

import pytest

from supriya.contexts import ContextObject, Server
from supriya.patterns.events import Event, GroupAllocateEvent, NodeFreeEvent, Priority

id_ = uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(NodeFreeEvent(id_), 0.0, [(0.0, Priority.START, NodeFreeEvent(id_))])],
)
def test_expand(
    event: Event, offset: float, expected: list[tuple[float, Priority, Event]]
) -> None:
    actual = event.expand(offset)
    assert actual == expected


def test_perform() -> None:
    context = Server().boot()
    proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject] = {}
    notes_mapping: dict[UUID | tuple[UUID, int], float] = {}
    # Allocate
    allocate_event = GroupAllocateEvent(id_)
    with context.at():
        allocate_event.perform(
            context,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    proxy = proxy_mapping[id_]
    # Wait
    context.sync()
    # Free
    free_event = NodeFreeEvent(id_)
    spy = Mock(wraps=context)
    with context.at():
        free_event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {}
    assert notes_mapping == {}
    assert spy.mock_calls == [call.free_node(proxy)]
