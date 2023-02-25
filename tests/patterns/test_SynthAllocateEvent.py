import uuid
from unittest.mock import Mock, call

import pytest

from supriya import AddAction
from supriya.assets.synthdefs import default
from supriya.contexts import Server, Synth
from supriya.patterns.events import Priority, SynthAllocateEvent

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [
        (
            SynthAllocateEvent(id_, default),
            0.0,
            [(0.0, Priority.START, SynthAllocateEvent(id_, default))],
        )
    ],
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
    event = SynthAllocateEvent(id_, default)
    with context.at():
        event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {id_: Synth(context=context, id_=1000, synthdef=default)}
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.add_synth(
            add_action=AddAction.ADD_TO_HEAD, synthdef=default, target_node=None
        )
    ]
