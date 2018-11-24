import pytest
import supriya
import uqbar.strings


def test_do_not_coerce_arguments():
    synth = supriya.realtime.Synth()
    group = supriya.realtime.Group()
    assert synth.node_id is None
    assert group.node_id is None
    request = supriya.commands.SynthNewRequest(
        node_id=synth, synthdef=synth.synthdef, target_node_id=group
    )
    assert request.node_id is synth
    assert request.target_node_id is group
    assert synth.node_id is None
    assert group.node_id is None
    with pytest.raises(TypeError):
        request.to_osc()


def test_allocate_ids_before_remote_application(server):
    """
    Local application allocates the synth's ID before we generate the OSC
    message.
    """
    synth = supriya.realtime.Synth()
    group = supriya.realtime.Group().allocate()
    assert synth.node_id is None
    assert group.node_id == 1000
    request = supriya.commands.SynthNewRequest(
        node_id=synth, synthdef=synth.synthdef, target_node_id=group
    )
    assert request.node_id is synth
    assert request.target_node_id is group
    with server.osc_io.capture() as transcript:
        request.communicate()
    assert list(transcript) == [
        ("S", supriya.osc.OscMessage(9, "default", 1001, 0, 1000)),
        ("R", supriya.osc.OscMessage("/n_go", 1001, 1000, -1, -1, 0)),
    ]
    assert synth.node_id == 1001
    assert synth.parent is group
    assert synth.is_allocated


def test_no_preexisting_synth_object(server):
    """
    Communicating without a pre-existing synth creates that synth during local
    application.
    """
    synthdef = supriya.assets.synthdefs.test.allocate()
    group = supriya.realtime.Group().allocate()
    request = supriya.commands.SynthNewRequest(
        node_id=666, synthdef=synthdef, target_node_id=group
    )
    assert request.node_id == 666
    with server.osc_io.capture() as transcript:
        request.communicate()
    assert list(transcript) == [
        ("S", supriya.osc.OscMessage(9, "test", 666, 0, 1000)),
        ("R", supriya.osc.OscMessage("/n_go", 666, 1000, -1, -1, 0)),
    ]
    synth = server[666]
    assert synth.parent is group
    assert synth.synthdef is synthdef


def test_bus_symbol_mapping(server):
    synthdef = supriya.assets.synthdefs.test.allocate()
    group = supriya.realtime.Group().allocate()
    request = supriya.commands.SynthNewRequest(
        node_id=666,
        synthdef=synthdef,
        target_node_id=group,
        amplitude="c0",
        frequency="a1",
    )
    with server.osc_io.capture() as transcript:
        request.communicate()
    assert list(transcript) == [
        (
            "S",
            supriya.osc.OscMessage(
                9, "test", 666, 0, 1000, "amplitude", "c0", "frequency", "a1"
            ),
        ),
        ("R", supriya.osc.OscMessage("/n_go", 666, 1000, -1, -1, 0)),
    ]
    synth = server[666]
    assert synth.parent is group
    assert synth.synthdef is synthdef
    assert str(synth.controls["amplitude"].value) == "c0"
    assert str(synth.controls["frequency"].value) == "a1"
    server_state = str(server.query_remote_nodes(True))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    666 test
                        amplitude: c0, frequency: a1
        """
    )
    assert str(server.query_local_nodes(True)) == server_state
