import types
import uuid

import pytest
import uqbar.strings

import supriya.patterns
import supriya.realtime


def test__perform_realtime_01(server):
    bus_uuid = uuid.uuid4()
    event = supriya.patterns.BusEvent(
        calculation_rate="audio", channel_count=2, uuid=bus_uuid
    )
    server = types.SimpleNamespace(
        audio_bus_allocator=supriya.realtime.BlockAllocator(),
        control_bus_allocator=supriya.realtime.BlockAllocator(),
    )
    uuids = {}
    event_products = event._perform_realtime(
        server=server, timestamp=100.0, uuids=uuids
    )
    assert pytest.helpers.get_objects_as_string(
        event_products, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        EventProduct(
            event=BusEvent(
                calculation_rate=CalculationRate.AUDIO,
                channel_count=2,
                uuid=UUID('A'),
            ),
            requests=[],
            timestamp=100.0,
            uuid=UUID('A'),
        )
        """
    )
    assert bus_uuid in uuids
    assert isinstance(uuids[bus_uuid], dict)
    assert list(uuids[bus_uuid].keys()) == [0]


def test__perform_realtime_02(server):
    bus_uuid = uuid.uuid4()
    event = supriya.patterns.BusEvent(is_stop=True, uuid=bus_uuid)
    server = types.SimpleNamespace(
        audio_bus_allocator=supriya.realtime.BlockAllocator(),
        control_bus_allocator=supriya.realtime.BlockAllocator(),
    )
    uuids = {
        bus_uuid: {0: supriya.realtime.BusGroup(calculation_rate="audio", bus_count=2)}
    }
    event_products = event._perform_realtime(
        server=server, timestamp=100.0, uuids=uuids
    )
    assert pytest.helpers.get_objects_as_string(
        event_products, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        EventProduct(
            event=BusEvent(
                calculation_rate=None,
                channel_count=None,
                is_stop=True,
                uuid=UUID('A'),
            ),
            is_stop=True,
            requests=[],
            timestamp=100.0,
            uuid=UUID('A'),
        )
        """
    )
