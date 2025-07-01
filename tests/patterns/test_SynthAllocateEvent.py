from unittest.mock import Mock, call
from uuid import UUID, uuid4

import pytest
from pytest_mock import MockerFixture

from supriya import AddAction, Server, Synth, default
from supriya.contexts import ContextObject
from supriya.patterns.events import Event, Priority, SynthAllocateEvent

id_ = uuid4()


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
def test_expand(
    event: Event, offset: float, expected: list[tuple[float, Priority, Event]]
) -> None:
    actual = event.expand(offset)
    assert actual == expected


def test_perform(mocker: MockerFixture) -> None:
    context = Server().boot()
    spy = Mock(wraps=context)
    mocker.patch.object(context, "send")
    proxy_mapping: dict[UUID | tuple[UUID, int], ContextObject] = {}
    notes_mapping: dict[UUID | tuple[UUID, int], float] = {}
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
            add_action=AddAction.ADD_TO_HEAD,
            permanent=False,
            synthdef=default,
            target_node=None,
        )
    ]
