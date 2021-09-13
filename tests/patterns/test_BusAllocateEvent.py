import uuid
from unittest.mock import Mock, call

import pytest

from supriya import CalculationRate
from supriya.patterns.events import BusAllocateEvent, Priority
from supriya.providers import BusGroupProxy, Provider

id_ = uuid.uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [
        (
            BusAllocateEvent(id_, calculation_rate="control", channel_count=2),
            0.0,
            [
                (
                    0.0,
                    Priority.START,
                    BusAllocateEvent(id_, calculation_rate="control", channel_count=2),
                )
            ],
        ),
        (
            BusAllocateEvent(id_, calculation_rate="audio", channel_count=8),
            0.0,
            [
                (
                    0.0,
                    Priority.START,
                    BusAllocateEvent(id_, calculation_rate="audio", channel_count=8),
                )
            ],
        ),
    ],
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
    event = BusAllocateEvent(id_, calculation_rate="audio", channel_count=8)
    with provider.at():
        event.perform(
            spy,
            proxy_mapping,
            current_offset=0.0,
            notes_mapping=notes_mapping,
            priority=Priority.START,
        )
    assert proxy_mapping == {
        id_: BusGroupProxy(
            calculation_rate=CalculationRate.AUDIO,
            channel_count=8,
            identifier=16,
            provider=provider,
        )
    }
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.add_bus_group(calculation_rate=CalculationRate.AUDIO, channel_count=8)
    ]
