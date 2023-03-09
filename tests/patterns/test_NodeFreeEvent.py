import uuid
from unittest.mock import Mock, call

import pytest

from supriya.contexts import Server
from supriya.patterns.events import GroupAllocateEvent, NodeFreeEvent, Priority

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(NodeFreeEvent(id_), 0.0, [(0.0, Priority.START, NodeFreeEvent(id_))])],
)
def test_expand(event, offset, expected):
    actual = event.expand(offset)
    assert actual == expected


def test_perform():
    context = Server().boot()
    proxy_mapping = {}
    notes_mapping = {}
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
