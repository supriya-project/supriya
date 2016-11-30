# -*- encoding: utf-8 -*-
import types
from abjad.tools import systemtools
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(systemtools.TestCase):

    def test__perform_realtime_01(self):
        event = patterntools.NoteEvent(
            duration=1.0,
            delta=10.0,
            frequency=443,
            )
        server = types.SimpleNamespace(
            node_id_allocator=servertools.NodeIdAllocator(),
            )
        start_product, stop_product = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids={},
            )
        assert start_product.uuid == stop_product.uuid
        self.compare_strings(
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=443,
                    is_stop=True,
                    ),
                index=0,
                is_stop=False,
                requests=[
                    supriya.tools.requesttools.SynthNewRequest(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_HEAD,
                        node_id=1000,
                        synthdef=<supriya.tools.synthdeftools.SynthDef('da0982184cc8fa54cf9d288a0fe1f6ca')>,
                        target_node_id=1,
                        frequency=443,
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('...'),
                )
            ''',
            format(start_product),
            )
        self.compare_strings(
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=443,
                    is_stop=True,
                    ),
                index=0,
                is_stop=True,
                requests=[
                    supriya.tools.requesttools.NodeSetRequest(
                        node_id=1000,
                        gate=0,
                        ),
                    ],
                timestamp=101.0,
                uuid=UUID('...'),
                )
            ''',
            format(stop_product),
            )

    def test__perform_realtime_02(self):
        event = patterntools.NoteEvent(
            duration=1.0,
            delta=10.0,
            frequency=[443, 445, 447],
            )
        server = types.SimpleNamespace(
            node_id_allocator=servertools.NodeIdAllocator(),
            )
        start_product, stop_product = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids={},
            )
        assert start_product.uuid == stop_product.uuid
        self.compare_strings(
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=[443, 445, 447],
                    is_stop=True,
                    ),
                index=0,
                is_stop=False,
                requests=[
                    supriya.tools.requesttools.SynthNewRequest(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_HEAD,
                        node_id=1000,
                        synthdef=<supriya.tools.synthdeftools.SynthDef('da0982184cc8fa54cf9d288a0fe1f6ca')>,
                        target_node_id=1,
                        frequency=443,
                        ),
                    supriya.tools.requesttools.SynthNewRequest(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_HEAD,
                        node_id=1001,
                        synthdef=<supriya.tools.synthdeftools.SynthDef('da0982184cc8fa54cf9d288a0fe1f6ca')>,
                        target_node_id=1,
                        frequency=445,
                        ),
                    supriya.tools.requesttools.SynthNewRequest(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_HEAD,
                        node_id=1002,
                        synthdef=<supriya.tools.synthdeftools.SynthDef('da0982184cc8fa54cf9d288a0fe1f6ca')>,
                        target_node_id=1,
                        frequency=447,
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('...'),
                )
            ''',
            format(start_product),
            )
        self.compare_strings(
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=[443, 445, 447],
                    is_stop=True,
                    ),
                index=0,
                is_stop=True,
                requests=[
                    supriya.tools.requesttools.NodeSetRequest(
                        node_id=1000,
                        gate=0,
                        ),
                    supriya.tools.requesttools.NodeSetRequest(
                        node_id=1001,
                        gate=0,
                        ),
                    supriya.tools.requesttools.NodeSetRequest(
                        node_id=1002,
                        gate=0,
                        ),
                    ],
                timestamp=101.0,
                uuid=UUID('...'),
                )
            ''',
            format(stop_product),
            )
