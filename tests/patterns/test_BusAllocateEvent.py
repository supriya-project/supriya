from unittest.mock import Mock, call
from uuid import UUID, uuid4

import pytest

from supriya.contexts import BusGroup, ContextObject, Server
from supriya.enums import CalculationRate
from supriya.patterns.events import BusAllocateEvent, Event, Priority

id_ = uuid4()


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
    event = BusAllocateEvent(id_, calculation_rate="audio", channel_count=8)
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
            calculation_rate=CalculationRate.AUDIO,
        )
    }
    assert notes_mapping == {}
    assert spy.mock_calls == [
        call.add_bus_group(calculation_rate=CalculationRate.AUDIO, count=8)
    ]
