from supriya.xdaw import Application, Track


def test_1():
    track_a = Track()
    track_b = Track()
    group_track = Track.group([track_a, track_b])
    group_track.ungroup()
    assert list(group_track.tracks) == []
    assert track_a.parent is None
    assert track_b.parent is None


def test_2():
    application = Application()
    context = application.add_context()
    track_a = context.add_track()
    track_b = context.add_track()
    track_c = context.add_track()
    group_track = Track.group([track_b, track_c])
    track_b.move(group_track, 1)
    assert list(group_track.tracks) == [track_c, track_b]
    group_track.ungroup()
    assert list(context.tracks) == [track_a, track_c, track_b]
    assert list(group_track.tracks) == []
    assert group_track.application is None
    assert group_track.parent is None
    assert track_b.application is application
    assert track_b.parent is context.tracks
    assert track_c.application is application
    assert track_c.parent is context.tracks


def test_3():
    application = Application()
    context = application.add_context()
    track_a = context.add_track()
    track_b = context.add_track()
    track_c = context.add_track()
    application.boot()
    group_track = Track.group([track_b, track_c])
    track_b.move(group_track, 1)
    assert list(group_track.tracks) == [track_c, track_b]
    group_track.ungroup()
    assert list(context.tracks) == [track_a, track_c, track_b]
    assert list(group_track.tracks) == []
    assert group_track.application is None
    assert group_track.parent is None
    assert group_track.provider is None
    assert track_b.application is application
    assert track_b.parent is context.tracks
    assert track_b.provider is context.provider
    assert track_c.application is application
    assert track_c.parent is context.tracks
    assert track_c.provider is context.provider
