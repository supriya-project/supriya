from supriya.xdaw import Application


def test_1():
    """
    Add one track, delete it
    """
    application = Application()
    context = application.add_context()
    parent = context.add_track()
    track = parent.add_track()
    track.delete()
    assert list(parent.tracks) == []
    assert track.application is None
    assert track.graph_order == ()
    assert track.parent is None
    assert track.provider is None


def test_2():
    """
    Add two tracks, delete the first
    """
    application = Application()
    context = application.add_context()
    parent = context.add_track()
    track_one = parent.add_track()
    track_two = parent.add_track()
    track_one.delete()
    assert list(parent.tracks) == [track_two]
    assert track_one.application is None
    assert track_one.graph_order == ()
    assert track_one.parent is None
    assert track_one.provider is None
    assert track_two.application is context.application
    assert track_two.graph_order == (3, 0, 0, 0, 1, 0)
    assert track_two.parent is parent.tracks
    assert track_two.provider is context.provider


def test_3():
    """
    Add one track, boot, add second track, delete the first
    """
    application = Application()
    context = application.add_context()
    parent = context.add_track()
    track_one = parent.add_track()
    application.boot()
    track_two = parent.add_track()
    with context.provider.server.osc_io.capture() as transcript:
        track_one.delete()
    assert list(parent.tracks) == [track_two]
    assert track_one.application is None
    assert track_one.graph_order == ()
    assert track_one.parent is None
    assert track_one.provider is None
    assert track_two.application is context.application
    assert track_two.graph_order == (3, 0, 0, 0, 1, 0)
    assert track_two.parent is parent.tracks
    assert track_two.provider is context.provider
    assert len(transcript.sent_messages) == 1
    _, message = transcript.sent_messages[0]
    assert message.to_list() == [None, [[15, 1009, "gate", 0]]]
