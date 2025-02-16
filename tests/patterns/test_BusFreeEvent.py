import uuid
from unittest.mock import Mock, call

import pytest

from supriya.contexts import BusGroup, Server
from supriya.enums import CalculationRate
from supriya.patterns.events import BusAllocateEvent, BusFreeEvent, Priority

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(BusFreeEvent(id_), 0.0, [(0.0, Priority.START, BusFreeEvent(id_))])],
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
    allocate_event = BusAllocateEvent(id_, rate="audio", channel_count=8)
    with context.at():
        allocate_event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    # Free
    free_event = BusFreeEvent(id_)
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
    assert spy.mock_calls == [
        call.add_bus_group(rate=CalculationRate.AUDIO, count=8),
        call.free_bus_group(
            BusGroup(
                context=context,
                id_=16,
                rate=CalculationRate.AUDIO,
                count=8,
            )
        ),
    ]
