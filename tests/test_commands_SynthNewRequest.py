import pytest
import supriya


def test_1():
    synth = supriya.realtime.Synth()
    group = supriya.realtime.Group()
    assert synth.node_id is None
    assert group.node_id is None
    request = supriya.commands.SynthNewRequest(
        node_id=synth,
        synthdef=synth.synthdef,
        target_node_id=group,
        )
    assert request.node_id is synth
    assert request.target_node_id is group
    assert synth.node_id is None
    assert group.node_id is None
    with pytest.raises(TypeError):
        request.to_osc_message()


def test_2(server):
    """
    Local application allocates the synth's ID before we generate the OSC
    message.
    """
    synth = supriya.realtime.Synth()
    group = supriya.realtime.Group().allocate()
    assert synth.node_id is None
    assert group.node_id == 1000
    request = supriya.commands.SynthNewRequest(
        node_id=synth,
        synthdef=synth.synthdef,
        target_node_id=group,
        )
    assert request.node_id is synth
    assert request.target_node_id is group
    with server.osc_io.capture() as transcript:
        request.communicate()
    assert list(transcript) == [
        ('S', supriya.osc.OscMessage(9, 'default', 1001, 0, 1000)),
        ('R', supriya.osc.OscMessage('/n_go', 1001, 1000, -1, -1, 0)),
        ]
    assert synth.node_id == 1001
    assert synth.parent is group
    assert synth.is_allocated


def test_3(server):
    """
    Communicating without a pre-existing synth creates that synth during local
    application.
    """
    synthdef = supriya.assets.synthdefs.test.allocate()
    group = supriya.realtime.Group().allocate()
    request = supriya.commands.SynthNewRequest(
        node_id=666,
        synthdef=synthdef,
        target_node_id=group,
        )
    assert request.node_id == 666
    with server.osc_io.capture() as transcript:
        request.communicate()
    assert list(transcript) == [
        ('S', supriya.osc.OscMessage(9, 'test', 666, 0, 1000)),
        ('R', supriya.osc.OscMessage('/n_go', 666, 1000, -1, -1, 0)),
        ]
    synth = server[666]
    assert synth.parent is group
    assert synth.synthdef is synthdef
