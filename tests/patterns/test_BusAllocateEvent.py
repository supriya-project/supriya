import uuid
from unittest.mock import Mock, call

import pytest

from supriya.contexts import BusGroup, Server
from supriya.enums import CalculationRate
from supriya.patterns.events import BusAllocateEvent, Priority

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [
        (
            BusAllocateEvent(id_, rate="control", channel_count=2),
            0.0,
            [
                (
                    0.0,
                    Priority.START,
                    BusAllocateEvent(id_, rate="control", channel_count=2),
                )
            ],
        ),
        (
            BusAllocateEvent(id_, rate="audio", channel_count=8),
            0.0,
            [
                (
                    0.0,
                    Priority.START,
                    BusAllocateEvent(id_, rate="audio", channel_count=8),
                )
            ],
        ),
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
    event = BusAllocateEvent(id_, rate="audio", channel_count=8)
    with context.at():
        event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {
        id_: BusGroup(
            id_=16,
            context=context,
            count=8,
            rate=CalculationRate.AUDIO,
        )
    }
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.add_bus_group(rate=CalculationRate.AUDIO, count=8)
    ]
