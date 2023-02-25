import uuid
from unittest.mock import Mock, call

import pytest

from supriya import AddAction
from supriya.contexts import Group, Server
from supriya.patterns.events import GroupAllocateEvent, Priority

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(GroupAllocateEvent(id_), 0.0, [(0.0, Priority.START, GroupAllocateEvent(id_))])],
)
def test_expand(event, offset, expected):
    actual = event.expand(offset)
    assert actual == expected


def test_perform():
    context = Server().boot()
    spy = Mock(wraps=context)
    proxy_mapping = {}
    notes_mapping = {}
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
