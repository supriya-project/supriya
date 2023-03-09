import uuid
from unittest.mock import Mock, call

import pytest

from supriya import AddAction, CalculationRate
from supriya.assets.synthdefs import default
from supriya.contexts import BusGroup, Server, Synth
from supriya.patterns.events import BusAllocateEvent, NoteEvent, Priority

id_ = uuid.uuid4()
bus_id = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [
        (
            NoteEvent(id_),
            0.0,
            [
                (0.0, Priority.START, NoteEvent((id_, 0))),
                (1.0, Priority.STOP, NoteEvent((id_, 0))),
            ],
        ),
        (
            NoteEvent(id_, frequency=[440, 550]),
            0.0,
            [
                (0.0, Priority.START, NoteEvent((id_, 0), frequency=440)),
                (0.0, Priority.START, NoteEvent((id_, 1), frequency=550)),
                (1.0, Priority.STOP, NoteEvent((id_, 0), frequency=440)),
                (1.0, Priority.STOP, NoteEvent((id_, 1), frequency=550)),
            ],
        ),
        (
            NoteEvent(id_, frequency=[440, 550], amplitude=[0.5, 0.75, 1.0]),
            2.5,
            [
                (
                    2.5,
                    Priority.START,
                    NoteEvent((id_, 0), amplitude=0.5, frequency=440),
                ),
                (
                    2.5,
                    Priority.START,
                    NoteEvent((id_, 1), amplitude=0.75, frequency=550),
                ),
                (
                    2.5,
                    Priority.START,
                    NoteEvent((id_, 2), amplitude=1.0, frequency=440),
                ),
                (3.5, Priority.STOP, NoteEvent((id_, 0), amplitude=0.5, frequency=440)),
                (
                    3.5,
                    Priority.STOP,
                    NoteEvent((id_, 1), amplitude=0.75, frequency=550),
                ),
                (3.5, Priority.STOP, NoteEvent((id_, 2), amplitude=1.0, frequency=440)),
            ],
        ),
    ],
)
def test_expand(event, offset, expected):
    actual = event.expand(offset)
    assert actual == expected


def test_perform():
    context = Server().boot()
    proxy_mapping = {}
    notes_mapping = {}
    # 0: Allocate a bus for later
    bus_event = BusAllocateEvent(bus_id, calculation_rate="control")
    with context.at():
        bus_event.perform(
            context,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    # A: Allocate
    event_one = NoteEvent(id_)
    spy = Mock(wraps=context)
    with context.at():
        event_one.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {
        id_: Synth(context=context, id_=1000, synthdef=default),
        bus_id: BusGroup(
            context=context,
            id_=0,
            calculation_rate=CalculationRate.CONTROL,
            count=1,
        ),
    }
    assert notes_mapping == {id_: 1.0}
    assert spy.mock_calls == [
        call.add_synth(
            add_action=AddAction.ADD_TO_HEAD, synthdef=default, target_node=None
        )
    ]
    # Wait
    context.sync()
    # B: Already allocated, so update settings
    event_two = NoteEvent(id_, amplitude=bus_id, frequency=550)
    spy = Mock(wraps=context)
    with context.at():
        event_two.perform(
            spy,
            proxy_mapping,
            current_offset=1.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {
        id_: Synth(context=context, id_=1000, synthdef=default),
        bus_id: BusGroup(
            context=context,
            id_=0,
            count=1,
            calculation_rate=CalculationRate.CONTROL,
        ),
    }
    assert notes_mapping == {id_: 2.0}
    assert spy.mock_calls == [
        call.set_node(
            Synth(context=context, id_=1000, synthdef=default),
            amplitude=proxy_mapping[bus_id],
            frequency=550,
        )
    ]
    # C: Free, but stop time doesn't match: no-op
    spy = Mock(wraps=context)
    with context.at():
        event_one.perform(
            spy,
            proxy_mapping,
            current_offset=1.0,
            notes_mapping=notes_mapping,
            priority=Priority.STOP,
        )
    assert proxy_mapping == {
        id_: Synth(context=context, id_=1000, synthdef=default),
        bus_id: BusGroup(
            context=context,
            id_=0,
            calculation_rate=CalculationRate.CONTROL,
            count=1,
        ),
    }
    assert notes_mapping == {id_: 2.0}
    assert spy.mock_calls == []
    # D: Free, and stop time does match
    spy = Mock(wraps=context)
    with context.at():
        event_one.perform(
            spy,
            proxy_mapping,
            current_offset=2.0,
            notes_mapping=notes_mapping,
            priority=Priority.STOP,
        )
    assert proxy_mapping == {
        bus_id: BusGroup(
            context=context,
            id_=0,
            calculation_rate=CalculationRate.CONTROL,
            count=1,
        )
    }
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.free_node(Synth(context=context, id_=1000, synthdef=default))
    ]
