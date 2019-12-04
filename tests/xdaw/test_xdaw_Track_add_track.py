from supriya.osc import OscBundle, OscMessage
from supriya.xdaw import Application, Track


def test_1():
    """
    Add one track
    """
    application = Application()
    context = application.add_context()
    parent = context.add_track()
    track = parent.add_track()
    assert isinstance(track, Track)
    assert len(track.postfader_sends) == 1
    assert list(parent.tracks) == [track]
    assert track.application is context.application
    assert track.graph_order == (2, 0, 0, 0, 0, 0)
    assert track.parent is parent.tracks
    assert track.postfader_sends[0].effective_target is parent
    assert track.provider is context.provider


def test_2():
    """
    Add two tracks
    """
    application = Application()
    context = application.add_context()
    parent = context.add_track()
    track_one = parent.add_track()
    track_two = parent.add_track()
    assert list(parent.tracks) == [track_one, track_two]
    assert track_one.application is context.application
    assert track_one.graph_order == (2, 0, 0, 0, 0, 0)
    assert track_one.parent is parent.tracks
    assert track_one.provider is context.provider
    assert track_two.application is context.application
    assert track_two.graph_order == (2, 0, 0, 0, 0, 1)
    assert track_two.parent is parent.tracks
    assert track_two.provider is context.provider


def test_3():
    """
    Add one track, boot, add second track
    """
    application = Application()
    context = application.add_context()
    parent = context.add_track()
    track_one = parent.add_track()
    application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        track_two = parent.add_track()
    assert context.provider is not None
    assert len(transcript.sent_messages) == 1
    assert list(parent.tracks) == [track_one, track_two]
    assert track_one.application is context.application
    assert track_one.graph_order == (2, 0, 0, 0, 0, 0)
    assert track_one.parent is parent.tracks
    assert track_one.provider is context.provider
    assert track_two.application is context.application
    assert track_two.graph_order == (2, 0, 0, 0, 0, 1)
    assert track_two.parent is parent.tracks
    assert track_two.provider is context.provider
    _, message = transcript.sent_messages[0]
    assert message == OscBundle(
        contents=(
            OscMessage(21, 1052, 1, 1009),
            OscMessage(21, 1053, 0, 1052),
            OscMessage(
                9, "mixer/patch[fb,gain]/2x2", 1054, 1, 1052, "in_", 32.0, "out", 34.0
            ),
            OscMessage(9, "mixer/levels/2", 1055, 1, 1052, "out", 34.0),
            OscMessage(9, "mixer/levels/2", 1056, 1, 1052, "out", 34.0),
            OscMessage(
                9,
                "mixer/patch[gain,hard,replace]/2x2",
                1057,
                1,
                1052,
                "in_",
                34.0,
                "out",
                34.0,
            ),
            OscMessage(9, "mixer/levels/2", 1058, 1, 1052, "out", 34.0),
            OscMessage(21, 1059, 3, 1054),
            OscMessage(21, 1060, 3, 1053),
            OscMessage(21, 1061, 3, 1055),
            OscMessage(21, 1062, 2, 1057),
            OscMessage(21, 1063, 3, 1057),
            OscMessage(
                9, "mixer/patch[gain]/2x2", 1064, 0, 1063, "in_", 34.0, "out", 18.0
            ),
        )
    )
