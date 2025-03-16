from unittest.mock import Mock, call
from uuid import UUID, uuid4

import pytest

from supriya.contexts import BusGroup, ContextObject, Server
from supriya.enums import CalculationRate
from supriya.patterns.events import BusAllocateEvent, BusFreeEvent, Event, Priority

id_ = uuid4()


@pytest.mark.parametrize(
    "event, offset, expected",
    [(BusFreeEvent(id_), 0.0, [(0.0, Priority.START, BusFreeEvent(id_))])],
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
    allocate_event = BusAllocateEvent(id_, calculation_rate="audio", channel_count=8)
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
        call.add_bus_group(calculation_rate=CalculationRate.AUDIO, count=8),
        call.free_bus_group(
            BusGroup(
                context=context,
                id_=16,
                calculation_rate=CalculationRate.AUDIO,
                count=8,
            )
        ),
    ]
