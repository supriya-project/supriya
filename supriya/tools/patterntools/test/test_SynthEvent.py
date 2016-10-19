# -*- encoding: utf-8 -*-
import types
import uuid
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(systemtools.TestCase):

    def test__perform_realtime_01(self):
        node_uuid = uuid.uuid4()
        event = patterntools.SynthEvent(
            out=4,
            pan=0.25,
            synthdef=synthdefs.default,
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
        assert len(event_products) == 1
        self.compare_strings(
            """
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.SynthEvent(
                    delta=0,
                    out=4,
                    pan=0.25,
                    synthdef=<supriya.tools.synthdeftools.SynthDef('da0982184cc8fa54cf9d288a0fe1f6ca')>,
                    uuid=UUID('...'),
                    ),
                index=0,
                requests=[
                    supriya.tools.requesttools.SynthNewRequest(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_HEAD,
                        node_id=1000,
                        synthdef=<supriya.tools.synthdeftools.SynthDef('da0982184cc8fa54cf9d288a0fe1f6ca')>,
                        target_node_id=1,
                        out=4,
                        pan=0.25,
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('...'),
                )
            """,
            format(event_products[0]),
            )
        assert node_uuid in uuids
        assert isinstance(uuids[node_uuid], dict)
        assert list(uuids[node_uuid].keys()) == [1000]

    def test__perform_realtime_02(self):
        node_uuid = uuid.uuid4()
        event = patterntools.SynthEvent(
            is_stop=True,
            uuid=node_uuid,
            )
        server = types.SimpleNamespace(
            node_id_allocator=servertools.NodeIdAllocator(),
            )
        uuids = {
            node_uuid: {
                1000: servertools.Synth(synthdefs.default),
                },
            }
        event_products = event._perform_realtime(
            server=server,
            timestamp=100.0,
            uuids=uuids,
            )
        assert len(event_products) == 1
        self.compare_strings(
            """
            supriya.tools.patterntools.EventProduct(
                event=supriya.tools.patterntools.SynthEvent(
                    delta=0,
                    is_stop=True,
                    uuid=UUID('...'),
                    ),
                index=0,
                is_stop=True,
                requests=[
                    supriya.tools.requesttools.NodeFreeRequest(
                        node_ids=(1000,),
                        ),
                    ],
                timestamp=100.0,
                uuid=UUID('...'),
                )
            """,
            format(event_products[0]),
            )
