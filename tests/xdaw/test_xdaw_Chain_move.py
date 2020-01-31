from supriya.xdaw import Application, RackDevice


def test_1():
    """
    Unbooted, move one chain before another
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    chain_two = rack_device.add_chain()
    chain_two.move(rack_device, 0)
    assert list(rack_device.chains) == [chain_two, chain_one]


def test_2():
    """
    Booted, move one chain before another
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    chain_two = rack_device.add_chain()
    application.boot()
    with context.provider.server.osc_protocol.capture() as transcript:
        chain_two.move(rack_device, 0)
    assert list(rack_device.chains) == [chain_two, chain_one]
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [None, [[22, 1017, 1032]]]


def test_3():
    """
    Booted, with cross-referencing sends, move one chain before another
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    chain_two = rack_device.add_chain()
    chain_one.add_send(chain_two)
    chain_two.add_send(chain_one)
    application.boot()
    with context.provider.server.osc_protocol.capture() as transcript:
        chain_two.move(rack_device, 0)
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [
        None,
        [
            [9, "mixer/patch[gain]/2x2", 1078, 0, 1044, "in_", 28.0, "out", 24.0],
            [9, "mixer/patch[fb,gain]/2x2", 1079, 0, 1030, "in_", 24.0, "out", 26.0],
            [22, 1017, 1032],
            [15, 1046, "gate", 0],
            [15, 1047, "gate", 0],
        ],
    ]


def test_4():
    """
    Booted, move one chain from one rack device to another
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device_one = track.add_device(RackDevice)
    rack_device_two = track.add_device(RackDevice)
    chain = rack_device_one.add_chain()
    application.boot()
    with context.provider.server.osc_protocol.capture() as transcript:
        chain.move(rack_device_two, 0)
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [
        None,
        [
            [9, "mixer/patch[gain]/2x2", 1066, 0, 1030, "in_", 24.0, "out", 26.0],
            [23, 1035, 1018],
            [15, 1031, "gate", 0],
        ],
    ]
