import uuid
from unittest.mock import Mock, call

import pytest

from supriya import AddAction
from supriya.assets.synthdefs import default
from supriya.patterns.events import Priority, SynthAllocateEvent
from supriya.providers import Provider, SynthProxy

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(SynthAllocateEvent(id_), 0.0, [(0.0, Priority.START, SynthAllocateEvent(id_))])],
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
    event = SynthAllocateEvent(id_)
    with provider.at():
        event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {
        id_: SynthProxy(
            provider=provider, identifier=1000, synthdef=default, settings={}
        )
    }
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.add_synth(
            add_action=AddAction.ADD_TO_HEAD, synthdef=None, target_node=None
        )
    ]
