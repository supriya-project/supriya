import types
import uuid
from patterntools_testbase import TestCase
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(TestCase):

    def test__perform_realtime_01(self):
        node_uuid = uuid.uuid4()
        event = patterntools.GroupEvent(
            uuid=node_uuid,
            )
        server = types.SimpleNamespace(
            node_id_allocator=servertools.NodeIdAllocator(),
            )
        uuids = {}
        event_products = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids=uuids,
            )
        self.compare_objects_as_strings(
            event_products,
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.GroupEvent(
                    delta=0.0,
                    uuid=UUID('A'),
                    ),
                index=0,
                requests=[
                    supriya.tools.requesttools.GroupNewRequest(
                        add_action=AddAction.ADD_TO_HEAD,
                        node_id=1000,
                        target_node_id=1,
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('A'),
                )
            ''',
            replace_uuids=True,
            )
        assert node_uuid in uuids
        assert isinstance(uuids[node_uuid], dict)
        assert list(uuids[node_uuid].keys()) == [1000]

    def test__perform_realtime_02(self):
        node_uuid = uuid.uuid4()
        event = patterntools.GroupEvent(
            is_stop=True,
            uuid=node_uuid,
            )
        server = types.SimpleNamespace(
            node_id_allocator=servertools.NodeIdAllocator(),
            )
        uuids = {
            node_uuid: {
                1000: servertools.Group(),
                },
            }
        event_products = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids=uuids,
            )
        self.compare_objects_as_strings(
            event_products,
            '''
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.GroupEvent(
                    delta=0.0,
                    is_stop=True,
                    uuid=UUID('A'),
                    ),
                index=0,
                is_stop=True,
                requests=[
                    supriya.tools.requesttools.NodeFreeRequest(
                        node_ids=(1000,),
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('A'),
                )
            ''',
            replace_uuids=True,
            )
