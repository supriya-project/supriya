import pytest
from uqbar.strings import normalize

from supriya.daw import Application, GroupTrack


def test_01():
    def state():
        return {
            track.node.name: (track.is_muted, track.is_active)
            for track in [track_a, group_one, track_b, group_two, track_c, track_d]
        }

    application = Application()
    track_a = application.add_track(name="a")
    track_b = application.add_track(name="b")
    track_c = application.add_track(name="c")
    track_d = application.add_track(name="d")
    group_one = GroupTrack.group([track_b, track_c, track_d], name="one")
    group_two = GroupTrack.group([track_c, track_d], name="two")

    assert state() == {
        "one": (False, True),
        "two": (False, True),
        "a": (False, True),
        "b": (False, True),
        "c": (False, True),
        "d": (False, True),
    }

    track_a.mute()
    assert state() == {
        "one": (False, True),
        "two": (False, True),
        "a": (True, False),
        "b": (False, True),
        "c": (False, True),
        "d": (False, True),
    }

    group_one.mute()
    assert state() == {
        "one": (True, False),
        "two": (False, False),
        "a": (True, False),
        "b": (False, False),
        "c": (False, False),
        "d": (False, False),
    }

    track_b.mute()
    assert state() == {
        "one": (True, False),
        "two": (False, False),
        "a": (True, False),
        "b": (True, False),
        "c": (False, False),
        "d": (False, False),
    }

    group_two.mute()
    assert state() == {
        "one": (True, False),
        "two": (True, False),
        "a": (True, False),
        "b": (True, False),
        "c": (False, False),
        "d": (False, False),
    }

    track_c.mute()
    assert state() == {
        "one": (True, False),
        "two": (True, False),
        "a": (True, False),
        "b": (True, False),
        "c": (True, False),
        "d": (False, False),
    }

    track_b.unmute()
    assert state() == {
        "one": (True, False),
        "two": (True, False),
        "a": (True, False),
        "b": (False, False),
        "c": (True, False),
        "d": (False, False),
    }

    group_one.unmute()
    assert state() == {
        "one": (False, True),
        "two": (True, False),
        "a": (True, False),
        "b": (False, True),
        "c": (True, False),
        "d": (False, False),
    }

    group_two.unmute()
    assert state() == {
        "one": (False, True),
        "two": (False, True),
        "a": (True, False),
        "b": (False, True),
        "c": (True, False),
        "d": (False, True),
    }

    track_c.unmute()
    assert state() == {
        "one": (False, True),
        "two": (False, True),
        "a": (True, False),
        "b": (False, True),
        "c": (False, True),
        "d": (False, True),
    }


def test_02():
    application = Application()
    application.add_track(name="a")
    track_b = application.add_track(name="b")
    track_c = application.add_track(name="c")
    track_d = application.add_track(name="d")
    GroupTrack.group([track_b, track_c, track_d], name="one")
    track_two = GroupTrack.group([track_c, track_d], name="two")
    application.boot()

    base_layout = normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1003 group (a)
                    1004 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1005 group (device container)
                    1006 group (pre-fader sends)
                    1007 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1008 group (post-fader sends)
                        1058 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1009 group (one)
                    1010 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1011 group (track container)
                        1012 group (b)
                            1013 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                            1014 group (device container)
                            1015 group (pre-fader sends)
                            1016 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                            1017 group (post-fader sends)
                                1018 mixer/send/2x2 (to one)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 30.0
                        1019 group (two)
                            1020 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.1, out: 38.0
                            1021 group (track container)
                                1022 group (c)
                                    1023 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.1, out: 42.0
                                    1024 group (device container)
                                    1025 group (pre-fader sends)
                                    1026 mixer/track-output/2
                                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 42.0
                                    1027 group (post-fader sends)
                                        1028 mixer/send/2x2 (to two)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 42.0, lag: 0.1, out: 38.0
                                1029 group (d)
                                    1030 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.1, out: 46.0
                                    1031 group (device container)
                                    1032 group (pre-fader sends)
                                    1033 mixer/track-output/2
                                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 46.0
                                    1034 group (post-fader sends)
                                        1035 mixer/send/2x2 (to two)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 46.0, lag: 0.1, out: 38.0
                            1036 group (device container)
                            1037 group (pre-fader sends)
                            1038 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 38.0
                            1039 group (post-fader sends)
                                1040 mixer/send/2x2 (to one)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 38.0, lag: 0.1, out: 30.0
                    1041 group (device container)
                    1042 group (pre-fader sends)
                    1043 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1044 group (post-fader sends)
                        1059 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
            1045 group (return track container)
            1046 group (master track)
                1047 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1048 group (device container)
                1049 group (pre-fader sends)
                1050 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1051 group (post-fader sends)
            1052 group (cue track)
                1053 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1054 group (device container)
                1055 group (pre-fader sends)
                1056 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1057 group (post-fader sends)
        """
    )
    assert str(application.node) == base_layout

    track_two.mute()
    assert str(application.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1003 group (a)
                    1004 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1005 group (device container)
                    1006 group (pre-fader sends)
                    1007 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1008 group (post-fader sends)
                        1058 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1009 group (one)
                    1010 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1011 group (track container)
                        1012 group (b)
                            1013 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                            1014 group (device container)
                            1015 group (pre-fader sends)
                            1016 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                            1017 group (post-fader sends)
                                1018 mixer/send/2x2 (to one)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 30.0
                        1019 group (two)
                            1020 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.1, out: 38.0
                            1021 group (track container)
                                1022 group (c)
                                    1023 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.1, out: 42.0
                                    1024 group (device container)
                                    1025 group (pre-fader sends)
                                    1026 mixer/track-output/2
                                        active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 42.0
                                    1027 group (post-fader sends)
                                        1028 mixer/send/2x2 (to two)
                                            active: 0.0, gain: 0.0, gate: 1.0, in_: 42.0, lag: 0.1, out: 38.0
                                1029 group (d)
                                    1030 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.1, out: 46.0
                                    1031 group (device container)
                                    1032 group (pre-fader sends)
                                    1033 mixer/track-output/2
                                        active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 46.0
                                    1034 group (post-fader sends)
                                        1035 mixer/send/2x2 (to two)
                                            active: 0.0, gain: 0.0, gate: 1.0, in_: 46.0, lag: 0.1, out: 38.0
                            1036 group (device container)
                            1037 group (pre-fader sends)
                            1038 mixer/track-output/2
                                active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 38.0
                            1039 group (post-fader sends)
                                1040 mixer/send/2x2 (to one)
                                    active: 0.0, gain: 0.0, gate: 1.0, in_: 38.0, lag: 0.1, out: 30.0
                    1041 group (device container)
                    1042 group (pre-fader sends)
                    1043 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1044 group (post-fader sends)
                        1059 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
            1045 group (return track container)
            1046 group (master track)
                1047 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1048 group (device container)
                1049 group (pre-fader sends)
                1050 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1051 group (post-fader sends)
            1052 group (cue track)
                1053 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1054 group (device container)
                1055 group (pre-fader sends)
                1056 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1057 group (post-fader sends)
        """
    )

    track_two.unmute()
    assert str(application.node) == base_layout


@pytest.mark.parametrize("boot_here", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_03(boot_here):
    application = Application()

    if boot_here == 1:
        application.boot()

    track_a = application.add_track(name="a")
    assert not track_a.is_muted
    assert track_a.is_active

    if boot_here == 2:
        application.boot()

    track_a.mute()
    assert track_a.is_muted
    assert not track_a.is_active

    if boot_here == 3:
        application.boot()

    group_one = GroupTrack(name="one")
    track_b = group_one.add_track(name="b")
    assert not group_one.is_muted
    assert group_one.is_active
    assert not track_b.is_muted
    assert track_b.is_active

    if boot_here == 4:
        application.boot()

    group_two = GroupTrack(name="two")
    group_two.mute()
    assert group_two.is_muted
    assert not group_two.is_active

    if boot_here == 5:
        application.boot()

    application.tracks.append(group_two)
    assert track_a.is_muted
    assert not track_a.is_active
    assert group_two.is_muted
    assert not group_two.is_active

    if boot_here == 6:
        application.boot()

    group_two.tracks.append(group_one)
    assert track_a.is_muted
    assert not track_a.is_active
    assert group_two.is_muted
    assert not group_two.is_active
    assert not group_one.is_muted
    assert not group_one.is_active
    assert not track_b.is_muted
    assert not track_b.is_active

    if boot_here == 7:
        application.boot()

    track_a.unmute()
    assert not track_a.is_muted
    assert track_a.is_active
    assert group_two.is_muted
    assert not group_two.is_active
    assert not group_one.is_muted
    assert not group_one.is_active
    assert not track_b.is_muted
    assert not track_b.is_active

    if boot_here == 8:
        application.boot()

    group_two.unmute()
    assert not track_a.is_muted
    assert track_a.is_active
    assert not group_two.is_muted
    assert group_two.is_active
    assert not group_one.is_muted
    assert group_one.is_active
    assert not track_b.is_muted
    assert track_b.is_active

    if boot_here == 9:
        application.boot()

    assert not track_a.is_muted
    assert track_a.is_active
    assert not group_two.is_muted
    assert group_two.is_active
    assert not group_one.is_muted
    assert group_one.is_active
    assert not track_b.is_muted
    assert track_b.is_active
