import types
import uuid

import pytest
import uqbar.strings

import supriya.assets.synthdefs
import supriya.patterns
import supriya.realtime


def test__perform_realtime_01():
    node_uuid = uuid.uuid4()
    event = supriya.patterns.SynthEvent(
        out=4, pan=0.25, synthdef=supriya.assets.synthdefs.default, uuid=node_uuid
    )
    server = types.SimpleNamespace(node_id_allocator=supriya.realtime.NodeIdAllocator())
    uuids = {}
    event_products = event._perform_realtime(
        server=server, timestamp=100.0, uuids=uuids
    )
    assert pytest.helpers.get_objects_as_string(
        event_products, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        EventProduct(
            event=SynthEvent(
                out=4,
                pan=0.25,
                synthdef=<SynthDef: default>,
                uuid=UUID('A'),
                ),
            requests=[
                SynthNewRequest(
                    add_action=AddAction.ADD_TO_HEAD,
                    node_id=1000,
                    out=4,
                    pan=0.25,
                    synthdef=<SynthDef: default>,
                    target_node_id=1,
                    ),
                ],
            timestamp=100.0,
            uuid=UUID('A'),
            )
        """
    )
    assert node_uuid in uuids
    assert isinstance(uuids[node_uuid], dict)
    assert list(uuids[node_uuid].keys()) == [1000]


def test__perform_realtime_02():
    node_uuid = uuid.uuid4()
    event = supriya.patterns.SynthEvent(is_stop=True, uuid=node_uuid)
    server = types.SimpleNamespace(node_id_allocator=supriya.realtime.NodeIdAllocator())
    uuids = {
        node_uuid: {1000: supriya.realtime.Synth(supriya.assets.synthdefs.default)}
    }
    event_products = event._perform_realtime(
        server=server, timestamp=100.0, uuids=uuids
    )
    assert pytest.helpers.get_objects_as_string(
        event_products, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        EventProduct(
            event=SynthEvent(
                is_stop=True,
                uuid=UUID('A'),
                ),
            is_stop=True,
            requests=[
                NodeFreeRequest(
                    node_ids=(1000,),
                    ),
                ],
            timestamp=100.0,
            uuid=UUID('A'),
            )
        """
    )
