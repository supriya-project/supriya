from supriya.xdaw import Application


def test_1():
    """
    Unbooted, move one track before another
    """
    application = Application()
    context = application.add_context()
    track_one = context.add_track()
    track_two = context.add_track()
    track_two.move(context, 0)
    assert list(context.tracks) == [track_two, track_one]


def test_2():
    """
    Booted, move one track before another
    """
    application = Application()
    context = application.add_context()
    track_one = context.add_track()
    track_two = context.add_track()
    application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        track_two.move(context, 0)
    assert list(context.tracks) == [track_two, track_one]
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [None, [[22, 1001, 1016]]]


def test_3():
    """
    Booted, with cross-referencing sends, move one track before another
    """
    application = Application()
    context = application.add_context()
    track_one = context.add_track()
    track_two = context.add_track()
    track_one.add_send(track_two)
    track_two.add_send(track_one)
    application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        track_two.move(context, 0)
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [
        None,
        [
            [9, "mixer/patch[gain]/2x2", 1061, 0, 1029, "in_", 22.0, "out", 18.0],
            [9, "mixer/patch[fb,gain]/2x2", 1062, 0, 1015, "in_", 18.0, "out", 20.0],
            [22, 1001, 1016],
            [15, 1030, "gate", 0],
            [15, 1031, "gate", 0],
        ]
    ]


def test_4():
    """
    Booted, move one track inside another, reallocate custom send and default send
    """
    application = Application()
    context = application.add_context()
    track_one = context.add_track()
    track_two = context.add_track()
    track_three = context.add_track()
    track_three.add_send(track_two)
    application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        track_three.move(track_one, 0)
    assert list(context.tracks) == [track_one, track_two]
    assert list(track_one.tracks) == [track_three]
    assert track_three.parent is track_one.tracks
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [
        None,
        [
            [9, "mixer/patch[gain]/2x2", 1075, 0, 1043, "in_", 26.0, "out", 18.0],
            [9, "mixer/patch[gain]/2x2", 1076, 0, 1043, "in_", 26.0, "out", 22.0],
            [23, 1008, 1030],
            [15, 1060, "gate", 0],
            [15, 1044, "gate", 0],
        ]
    ]
