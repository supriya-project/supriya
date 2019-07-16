import time

from uqbar.strings import normalize

from supriya.daw import Application, GroupTrack


def test_01():
    app = Application()
    app.boot()
    track_a = app.add_track(name="track a")
    track_b = app.add_track(name="track b")
    track_c = app.add_track(name="track c")

    assert str(app.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1016 group (track a)
                    1017 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1018 group (device container)
                    1019 group (pre-fader sends)
                    1020 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1021 group (post-fader sends)
                        1022 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1023 group (track b)
                    1024 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1025 group (device container)
                    1026 group (pre-fader sends)
                    1027 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1028 group (post-fader sends)
                        1029 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
                1030 group (track c)
                    1031 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                    1032 group (device container)
                    1033 group (pre-fader sends)
                    1034 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                    1035 group (post-fader sends)
                        1036 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 22.0
            1003 group (return track container)
            1004 group (master track)
                1005 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1006 group (device container)
                1007 group (pre-fader sends)
                1008 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1009 group (post-fader sends)
            1010 group (cue track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1015 group (post-fader sends)
        """
    )

    group_track_a = GroupTrack.group([track_a, track_b, track_c])
    time.sleep(0.25)
    assert str(app.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1037 group (group track)
                    1038 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.1, out: 38.0
                    1039 group (track container)
                        1016 group (track a)
                            1017 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                            1018 group (device container)
                            1019 group (pre-fader sends)
                            1020 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                            1021 group (post-fader sends)
                                1045 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 38.0
                        1023 group (track b)
                            1024 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                            1025 group (device container)
                            1026 group (pre-fader sends)
                            1027 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                            1028 group (post-fader sends)
                                1046 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 38.0
                        1030 group (track c)
                            1031 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                            1032 group (device container)
                            1033 group (pre-fader sends)
                            1034 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                            1035 group (post-fader sends)
                                1047 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 38.0
                    1040 group (device container)
                    1041 group (pre-fader sends)
                    1042 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 38.0
                    1043 group (post-fader sends)
                        1044 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 38.0, lag: 0.1, out: 22.0
            1003 group (return track container)
            1004 group (master track)
                1005 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1006 group (device container)
                1007 group (pre-fader sends)
                1008 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1009 group (post-fader sends)
            1010 group (cue track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1015 group (post-fader sends)
        """
    )

    group_track_b = GroupTrack.group([track_c, track_b])
    time.sleep(0.25)
    assert str(app.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1037 group (group track)
                    1038 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.1, out: 38.0
                    1039 group (track container)
                        1016 group (track a)
                            1017 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                            1018 group (device container)
                            1019 group (pre-fader sends)
                            1020 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                            1021 group (post-fader sends)
                                1045 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 38.0
                        1048 group (group track)
                            1049 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.1, out: 42.0
                            1050 group (track container)
                                1030 group (track c)
                                    1031 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                                    1032 group (device container)
                                    1033 group (pre-fader sends)
                                    1034 mixer/track-output/2
                                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                                    1035 group (post-fader sends)
                                        1056 mixer/send/2x2 (to group track)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 42.0
                                1023 group (track b)
                                    1024 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                                    1025 group (device container)
                                    1026 group (pre-fader sends)
                                    1027 mixer/track-output/2
                                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                                    1028 group (post-fader sends)
                                        1057 mixer/send/2x2 (to group track)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 42.0
                            1051 group (device container)
                            1052 group (pre-fader sends)
                            1053 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 42.0
                            1054 group (post-fader sends)
                                1055 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 42.0, lag: 0.1, out: 38.0
                    1040 group (device container)
                    1041 group (pre-fader sends)
                    1042 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 38.0
                    1043 group (post-fader sends)
                        1044 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 38.0, lag: 0.1, out: 22.0
            1003 group (return track container)
            1004 group (master track)
                1005 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1006 group (device container)
                1007 group (pre-fader sends)
                1008 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1009 group (post-fader sends)
            1010 group (cue track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1015 group (post-fader sends)
        """
    )

    group_track_a.add_track(name="track d")
    assert str(app.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1037 group (group track)
                    1038 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.1, out: 38.0
                    1039 group (track container)
                        1016 group (track a)
                            1017 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                            1018 group (device container)
                            1019 group (pre-fader sends)
                            1020 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                            1021 group (post-fader sends)
                                1045 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 38.0
                        1048 group (group track)
                            1049 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.1, out: 42.0
                            1050 group (track container)
                                1030 group (track c)
                                    1031 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                                    1032 group (device container)
                                    1033 group (pre-fader sends)
                                    1034 mixer/track-output/2
                                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                                    1035 group (post-fader sends)
                                        1056 mixer/send/2x2 (to group track)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 42.0
                                1023 group (track b)
                                    1024 mixer/track-input/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                                    1025 group (device container)
                                    1026 group (pre-fader sends)
                                    1027 mixer/track-output/2
                                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                                    1028 group (post-fader sends)
                                        1057 mixer/send/2x2 (to group track)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 42.0
                            1051 group (device container)
                            1052 group (pre-fader sends)
                            1053 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 42.0
                            1054 group (post-fader sends)
                                1055 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 42.0, lag: 0.1, out: 38.0
                        1058 group (track d)
                            1059 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.1, out: 46.0
                            1060 group (device container)
                            1061 group (pre-fader sends)
                            1062 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 46.0
                            1063 group (post-fader sends)
                                1064 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 46.0, lag: 0.1, out: 38.0
                    1040 group (device container)
                    1041 group (pre-fader sends)
                    1042 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 38.0
                    1043 group (post-fader sends)
                        1044 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 38.0, lag: 0.1, out: 22.0
            1003 group (return track container)
            1004 group (master track)
                1005 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1006 group (device container)
                1007 group (pre-fader sends)
                1008 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1009 group (post-fader sends)
            1010 group (cue track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1015 group (post-fader sends)
        """
    )

    group_track_a.ungroup()
    time.sleep(0.25)
    assert str(app.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1016 group (track a)
                    1017 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1018 group (device container)
                    1019 group (pre-fader sends)
                    1020 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1021 group (post-fader sends)
                        1065 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1048 group (group track)
                    1049 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.1, out: 42.0
                    1050 group (track container)
                        1030 group (track c)
                            1031 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                            1032 group (device container)
                            1033 group (pre-fader sends)
                            1034 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                            1035 group (post-fader sends)
                                1056 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 42.0
                        1023 group (track b)
                            1024 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                            1025 group (device container)
                            1026 group (pre-fader sends)
                            1027 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                            1028 group (post-fader sends)
                                1057 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 42.0
                    1051 group (device container)
                    1052 group (pre-fader sends)
                    1053 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 42.0
                    1054 group (post-fader sends)
                        1066 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 42.0, lag: 0.1, out: 22.0
                1058 group (track d)
                    1059 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.1, out: 46.0
                    1060 group (device container)
                    1061 group (pre-fader sends)
                    1062 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 46.0
                    1063 group (post-fader sends)
                        1067 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 46.0, lag: 0.1, out: 22.0
            1003 group (return track container)
            1004 group (master track)
                1005 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1006 group (device container)
                1007 group (pre-fader sends)
                1008 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1009 group (post-fader sends)
            1010 group (cue track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1015 group (post-fader sends)
        """
    )

    group_track_b.ungroup()
    time.sleep(0.25)
    assert str(app.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1016 group (track a)
                    1017 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1018 group (device container)
                    1019 group (pre-fader sends)
                    1020 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1021 group (post-fader sends)
                        1065 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1030 group (track c)
                    1031 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                    1032 group (device container)
                    1033 group (pre-fader sends)
                    1034 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                    1035 group (post-fader sends)
                        1068 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 22.0
                1023 group (track b)
                    1024 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1025 group (device container)
                    1026 group (pre-fader sends)
                    1027 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1028 group (post-fader sends)
                        1069 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
                1058 group (track d)
                    1059 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.1, out: 46.0
                    1060 group (device container)
                    1061 group (pre-fader sends)
                    1062 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 46.0
                    1063 group (post-fader sends)
                        1067 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 46.0, lag: 0.1, out: 22.0
            1003 group (return track container)
            1004 group (master track)
                1005 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1006 group (device container)
                1007 group (pre-fader sends)
                1008 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1009 group (post-fader sends)
            1010 group (cue track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1015 group (post-fader sends)
        """
    )
