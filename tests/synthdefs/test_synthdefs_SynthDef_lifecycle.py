import pytest

import supriya
import supriya.assets.synthdefs


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


def test_unaggregated_anonymous(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build()
    assert synthdef not in server
    with server.osc_protocol.capture() as transcript:
        synthdef.allocate(server=server)
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage("/d_recv", synthdef.compile())
    ]
    with server.osc_protocol.capture() as transcript:
        synthdef.free(server)
    assert synthdef not in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage("/d_free", synthdef.anonymous_name)
    ]


def test_unaggregated_named(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build(name="test-synthdef")
    assert synthdef not in server
    with server.osc_protocol.capture() as transcript:
        synthdef.allocate(server=server)
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage("/d_recv", synthdef.compile())
    ]
    with server.osc_protocol.capture() as transcript:
        synthdef.free(server)
    assert synthdef not in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage("/d_free", synthdef.name)
    ]


def test_aggregated_anonymous(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build()
    assert synthdef not in server

    synth_a = supriya.Synth(synthdef=synthdef, frequency=666)
    synth_b = supriya.Synth(synthdef=synthdef, frequency=777)
    synth_c = supriya.Synth(synthdef=synthdef, frequency=888)

    # allocate synthdef on node allocation
    with server.osc_protocol.capture() as transcript:
        synth_a.allocate(server)
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            "/d_recv",
            synthdef.compile(),
            supriya.osc.OscMessage(
                "/s_new", synthdef.anonymous_name, 1000, 0, 1, "frequency", 666.0
            ),
        )
    ]

    # don't need to re-allocate
    with server.osc_protocol.capture() as transcript:
        synth_b.allocate(server)
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            "/s_new", synthdef.anonymous_name, 1001, 0, 1, "frequency", 777.0
        )
    ]

    # just free the synthdef
    with server.osc_protocol.capture() as transcript:
        synthdef.free(server)
    assert synthdef not in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage("/d_free", synthdef.anonymous_name)
    ]

    # allocate synthdef (again)n on node allocation
    with server.osc_protocol.capture() as transcript:
        synth_c.allocate(server)
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            "/d_recv",
            synthdef.compile(),
            supriya.osc.OscMessage(
                "/s_new", synthdef.anonymous_name, 1002, 0, 1, "frequency", 888.0
            ),
        )
    ]


def test_aggregated_named(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build(name="test-synthdef")
    assert synthdef not in server

    synth_a = supriya.Synth(synthdef=synthdef, frequency=666)
    synth_b = supriya.Synth(synthdef=synthdef, frequency=777)
    synth_c = supriya.Synth(synthdef=synthdef, frequency=888)

    # allocate synthdef on node allocation
    with server.osc_protocol.capture() as transcript:
        synth_a.allocate(server)
    assert synthdef in server
    assert [
        message
        for timestamp, message in transcript.sent_messages
        if message.address not in ("/status",)
    ] == [
        supriya.osc.OscMessage(
            "/d_recv",
            synthdef.compile(),
            supriya.osc.OscMessage(
                "/s_new", synthdef.name, 1000, 0, 1, "frequency", 666.0
            ),
        )
    ]

    # don't need to re-allocate
    with server.osc_protocol.capture() as transcript:
        synth_b.allocate(server)
    assert synthdef in server
    assert [
        message
        for timestamp, message in transcript.sent_messages
        if message.address not in ("/status",)
    ] == [
        supriya.osc.OscMessage("/s_new", synthdef.name, 1001, 0, 1, "frequency", 777.0)
    ]

    # just free the synthdef
    with server.osc_protocol.capture() as transcript:
        synthdef.free(server)
    assert synthdef not in server
    assert [
        message
        for timestamp, message in transcript.sent_messages
        if message.address not in ("/status",)
    ] == [supriya.osc.OscMessage("/d_free", synthdef.name)]

    # allocate synthdef (again)n on node allocation
    with server.osc_protocol.capture() as transcript:
        synth_c.allocate(server)
    assert synthdef in server
    assert [
        message
        for timestamp, message in transcript.sent_messages
        if message.address not in ("/status",)
    ] == [
        supriya.osc.OscMessage(
            "/d_recv",
            synthdef.compile(),
            supriya.osc.OscMessage(
                "/s_new", synthdef.name, 1002, 0, 1, "frequency", 888.0
            ),
        )
    ]
