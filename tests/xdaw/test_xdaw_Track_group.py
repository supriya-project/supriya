from supriya.xdaw import Application, Track


def test_1():
    track_a = Track()
    track_b = Track()
    group_track = Track.group([track_a, track_b])
    assert isinstance(group_track, Track)
    assert list(group_track.tracks) == [track_a, track_b]
    assert group_track.application is track_a.application
    assert group_track.channel_count is None
    assert group_track.name is None
    assert group_track.parent is None
    assert group_track.provider is track_a.provider
    assert not group_track.is_cued
    assert not group_track.is_muted
    assert not group_track.is_soloed
    assert track_a.parent is group_track.tracks
    assert track_b.parent is group_track.tracks


def test_2():
    application = Application()
    context = application.add_context()
    track_a = context.add_track()
    track_b = context.add_track()
    track_c = context.add_track()
    group_track = Track.group([track_b, track_c])
    assert list(context.tracks) == [track_a, group_track]
    assert list(group_track.tracks) == [track_b, track_c]
    assert group_track.application is application
    assert group_track.parent is context.tracks
    assert group_track.provider is context.provider
    assert track_b.provider is context.provider
    assert track_c.provider is context.provider


def test_3():
    application = Application()
    context = application.add_context()
    track_a = context.add_track()
    track_b = context.add_track()
    track_c = context.add_track()
    application.boot()
    group_track = Track.group([track_b, track_c])
    assert list(context.tracks) == [track_a, group_track]
    assert list(group_track.tracks) == [track_b, track_c]
    assert group_track.application is application
    assert group_track.parent is context.tracks
    assert group_track.provider is context.provider
    assert track_b.provider is context.provider
    assert track_c.provider is context.provider
