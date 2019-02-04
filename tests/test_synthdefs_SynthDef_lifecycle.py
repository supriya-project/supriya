import supriya


def test_unaggregated_anonymous(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build()
    assert synthdef.server is None
    assert synthdef not in server
    with server.osc_io.capture() as transcript:
        synthdef.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(5, synthdef.compile())
    ]
    with server.osc_io.capture() as transcript:
        synthdef.free()
    assert synthdef.server is None
    assert synthdef not in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(53, synthdef.anonymous_name)
    ]


def test_unaggregated_named(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build(name="test-synthdef")
    assert synthdef.server is None
    assert synthdef not in server
    with server.osc_io.capture() as transcript:
        synthdef.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(5, synthdef.compile())
    ]
    with server.osc_io.capture() as transcript:
        synthdef.free()
    assert synthdef.server is None
    assert synthdef not in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(53, synthdef.name)
    ]


def test_aggregated_anonymous(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build()
    assert synthdef.server is None
    assert synthdef not in server

    synth_a = supriya.Synth(synthdef=synthdef, frequency=666)
    synth_b = supriya.Synth(synthdef=synthdef, frequency=777)
    synth_c = supriya.Synth(synthdef=synthdef, frequency=888)

    # allocate synthdef on node allocation
    with server.osc_io.capture() as transcript:
        synth_a.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            5,
            synthdef.compile(),
            supriya.osc.OscMessage(
                9, synthdef.anonymous_name, 1000, 0, 1, "frequency", 666.0
            ),
        )
    ]

    # don't need to re-allocate
    with server.osc_io.capture() as transcript:
        synth_b.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            9, synthdef.anonymous_name, 1001, 0, 1, "frequency", 777.0
        )
    ]

    # just free the synthdef
    with server.osc_io.capture() as transcript:
        synthdef.free()
    assert synthdef.server is None
    assert synthdef not in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(53, synthdef.anonymous_name)
    ]

    # allocate synthdef (again)n on node allocation
    with server.osc_io.capture() as transcript:
        synth_c.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            5,
            synthdef.compile(),
            supriya.osc.OscMessage(
                9, synthdef.anonymous_name, 1002, 0, 1, "frequency", 888.0
            ),
        )
    ]


def test_aggregated_named(server):
    with supriya.SynthDefBuilder(frequency=440) as builder:
        source = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        supriya.ugens.Out.ar(bus=0, source=source)
    synthdef = builder.build(name="test-synthdef")
    assert synthdef.server is None
    assert synthdef not in server

    synth_a = supriya.Synth(synthdef=synthdef, frequency=666)
    synth_b = supriya.Synth(synthdef=synthdef, frequency=777)
    synth_c = supriya.Synth(synthdef=synthdef, frequency=888)

    # allocate synthdef on node allocation
    with server.osc_io.capture() as transcript:
        synth_a.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            5,
            synthdef.compile(),
            supriya.osc.OscMessage(9, synthdef.name, 1000, 0, 1, "frequency", 666.0),
        )
    ]

    # don't need to re-allocate
    with server.osc_io.capture() as transcript:
        synth_b.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(9, synthdef.name, 1001, 0, 1, "frequency", 777.0)
    ]

    # just free the synthdef
    with server.osc_io.capture() as transcript:
        synthdef.free()
    assert synthdef.server is None
    assert synthdef not in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(53, synthdef.name)
    ]

    # allocate synthdef (again)n on node allocation
    with server.osc_io.capture() as transcript:
        synth_c.allocate(server=server)
    assert synthdef.server is server
    assert synthdef in server
    assert [message for timestamp, message in transcript.sent_messages] == [
        supriya.osc.OscMessage(
            5,
            synthdef.compile(),
            supriya.osc.OscMessage(9, synthdef.name, 1002, 0, 1, "frequency", 888.0),
        )
    ]
