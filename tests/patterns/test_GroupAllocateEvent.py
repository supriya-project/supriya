from unittest.mock import Mock, call
from uuid import UUID, uuid4

import pytest

from supriya import AddAction
from supriya.contexts import ContextObject, Group, Server
from supriya.patterns.events import Event, GroupAllocateEvent, Priority

id_ = uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(GroupAllocateEvent(id_), 0.0, [(0.0, Priority.START, GroupAllocateEvent(id_))])],
)
def test_expand(
    event: Event, offset: float, expected: list[tuple[float, Priority, Event]]
) -> None:
    actual = event.expand(offset)
    assert actual == expected


def test_perform() -> None:
    context = Server().boot()
    spy = Mock(wraps=context)
    proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject] = {}
    notes_mapping: dict[UUID | tuple[UUID, int], float] = {}
    # Allocate
    event = GroupAllocateEvent(id_)
    with context.at():
        event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {id_: Group(context=context, id_=1000)}
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.add_group(add_action=AddAction.ADD_TO_HEAD, target_node=None)
    ]
