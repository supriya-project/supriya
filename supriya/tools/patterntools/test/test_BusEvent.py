# -*- encoding: utf-8 -*-
import types
import uuid
from abjad.tools import systemtools
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(systemtools.TestCase):

    def test__perform_realtime_01(self):
        bus_uuid = uuid.uuid4()
        event = patterntools.BusEvent(
            calculation_rate='audio',
            channel_count=2,
            uuid=bus_uuid,
            )
        server = types.SimpleNamespace(
            audio_bus_allocator=servertools.BlockAllocator(),
            control_bus_allocator=servertools.BlockAllocator(),
            )
        uuids = {}
        event_products = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids=uuids,
            )
        assert len(event_products) == 1
        self.compare_strings(
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.BusEvent(
                    calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                    channel_count=2,
                    delta=0,
                    uuid=UUID('...'),
                    ),
                index=0,
                requests=[],
                timestamp=100.0,
                uuid=UUID('...'),
                )
            ''',
            format(event_products[0]),
            )
        assert bus_uuid in uuids
        assert isinstance(uuids[bus_uuid], dict)
        assert list(uuids[bus_uuid].keys()) == [0]

    def test__perform_realtime_02(self):
        bus_uuid = uuid.uuid4()
        event = patterntools.BusEvent(
            calculation_rate='audio',
            channel_count=2,
            is_stop=True,
            release_time=0,
            uuid=bus_uuid,
            )
        server = types.SimpleNamespace(
            audio_bus_allocator=servertools.BlockAllocator(),
            control_bus_allocator=servertools.BlockAllocator(),
            )
        uuids = {
            bus_uuid: {
                0: servertools.BusGroup(
                    calculation_rate='audio',
                    bus_count=2,
                    )
                },
            }
        event_products = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids=uuids,
            )
        assert len(event_products) == 1
        self.compare_strings(
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.BusEvent(
                    calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                    channel_count=2,
                    delta=0,
                    is_stop=True,
                    release_time=0,
                    uuid=UUID('...'),
                    ),
                index=0,
                is_stop=True,
                requests=[],
                timestamp=100.0,
                uuid=UUID('...'),
                )
            ''',
            format(event_products[0]),
            )
