import types
import uqbar.strings
from patterns_testbase import TestCase
import supriya.patterns
import supriya.realtime


class TestCase(TestCase):

    def test__perform_realtime_01(self):
        event = supriya.patterns.NoteEvent(
            duration=1.0,
            delta=10.0,
            frequency=443,
            )
        server = types.SimpleNamespace(
            node_id_allocator=supriya.realtime.NodeIdAllocator(),
            )
        event_products = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids={},
            )
        assert event_products[0].uuid == event_products[1].uuid
        assert self.get_objects_as_string(
            event_products,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            EventProduct(
                event=NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=443,
                    ),
                requests=[
                    SynthNewRequest(
                        add_action=AddAction.ADD_TO_HEAD,
                        frequency=443,
                        node_id=1000,
                        synthdef=<SynthDef: default>,
                        target_node_id=1,
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('A'),
                )
            EventProduct(
                event=NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=443,
                    ),
                is_stop=True,
                requests=[
                    NodeSetRequest(
                        gate=0,
                        node_id=1000,
                        ),
                    ],
                timestamp=101.0,
                uuid=UUID('A'),
                )
            ''')

    def test__perform_realtime_02(self):
        event = supriya.patterns.NoteEvent(
            duration=1.0,
            delta=10.0,
            frequency=[443, 445, 447],
            )
        server = types.SimpleNamespace(
            node_id_allocator=supriya.realtime.NodeIdAllocator(),
            )
        event_products = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids={},
            )
        assert self.get_objects_as_string(
            event_products,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            EventProduct(
                event=NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=[443, 445, 447],
                    ),
                requests=[
                    SynthNewRequest(
                        add_action=AddAction.ADD_TO_HEAD,
                        frequency=443,
                        node_id=1000,
                        synthdef=<SynthDef: default>,
                        target_node_id=1,
                        ),
                    SynthNewRequest(
                        add_action=AddAction.ADD_TO_HEAD,
                        frequency=445,
                        node_id=1001,
                        synthdef=<SynthDef: default>,
                        target_node_id=1,
                        ),
                    SynthNewRequest(
                        add_action=AddAction.ADD_TO_HEAD,
                        frequency=447,
                        node_id=1002,
                        synthdef=<SynthDef: default>,
                        target_node_id=1,
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('A'),
                )
            EventProduct(
                event=NoteEvent(
                    delta=10.0,
                    duration=1.0,
                    frequency=[443, 445, 447],
                    ),
                is_stop=True,
                requests=[
                    NodeSetRequest(
                        gate=0,
                        node_id=1000,
                        ),
                    NodeSetRequest(
                        gate=0,
                        node_id=1001,
                        ),
                    NodeSetRequest(
                        gate=0,
                        node_id=1002,
                        ),
                    ],
                timestamp=101.0,
                uuid=UUID('A'),
                )
            ''')
