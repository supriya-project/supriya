from supriya.osc import OscBundle, OscMessage
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
    assert message == OscBundle(contents=(OscMessage(22, 1001, 1014),))


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
    assert message == OscBundle(
        contents=(
            OscMessage(
                9, "mix/patch[gain]/2x2", 1054, 0, 1025, "in_", 22.0, "out", 18.0
            ),
            OscMessage(
                9, "mix/patch[fb,gain]/2x2", 1055, 0, 1013, "in_", 18.0, "out", 20.0
            ),
            OscMessage(22, 1001, 1014),
            OscMessage(15, 1026, "gate", 0),
            OscMessage(15, 1027, "gate", 0),
        )
    )


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
    assert message == OscBundle(
        contents=(
            OscMessage(
                9, "mix/patch[gain]/2x2", 1066, 0, 1037, "in_", 26.0, "out", 18.0
            ),
            OscMessage(
                9, "mix/patch[gain]/2x2", 1067, 0, 1037, "in_", 26.0, "out", 22.0
            ),
            OscMessage(23, 1009, 1026),
            OscMessage(15, 1053, "gate", 0),
            OscMessage(15, 1038, "gate", 0),
        )
    )
