import uuid
from unittest.mock import Mock, call

import pytest

from supriya import AddAction
from supriya.patterns.events import GroupAllocateEvent, Priority
from supriya.providers import GroupProxy, Provider

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(GroupAllocateEvent(id_), 0.0, [(0.0, Priority.START, GroupAllocateEvent(id_))])],
)
def test_expand(event, offset, expected):
    actual = event.expand(offset)
    assert actual == expected


def test_perform():
    provider = Provider.realtime()
    spy = Mock(wraps=provider)
    proxy_mapping = {}
    notes_mapping = {}
    # Allocate
    event = GroupAllocateEvent(id_)
    with provider.at():
        event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {id_: GroupProxy(provider=provider, identifier=1000)}
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.add_group(add_action=AddAction.ADD_TO_HEAD, target_node=None)
    ]
