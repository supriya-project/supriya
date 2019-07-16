import time

from uqbar.strings import normalize

from supriya.daw import Application


def test_01():
    # TODO: The sends should reallocate after the move to ensure correct bus usage
    print("Yes...")
    application = Application()
    application.boot()
    track_one = application.add_track(name="one")
    track_two = application.add_track(name="two")
    track_one.add_send(track_two, post_fader=False)
    track_two.add_send(track_one, post_fader=False)
    assert application.tracks[:] == [track_one, track_two]
    assert str(application.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1016 group (one)
                    1017 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1018 group (device container)
                    1019 group (pre-fader sends)
                        1030 mixer/send/2x2 (to two)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 30.0
                    1020 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1021 group (post-fader sends)
                        1022 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1023 group (two)
                    1024 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1025 group (device container)
                    1026 group (pre-fader sends)
                        1031 mixer/send/2x2 (to one)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 24.0
                    1027 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1028 group (post-fader sends)
                        1029 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
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
    print()
    print("Moving...")
    print()
    application.tracks[:] = [track_two, track_one]
    assert application.tracks[:] == [track_two, track_one]
    time.sleep(0.25)
    assert str(application.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1023 group (two)
                    1024 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1025 group (device container)
                    1026 group (pre-fader sends)
                        1033 mixer/send/2x2 (to one)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 26.0
                    1027 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1028 group (post-fader sends)
                        1029 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
                1016 group (one)
                    1017 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1018 group (device container)
                    1019 group (pre-fader sends)
                        1032 mixer/send/2x2 (to two)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 28.0
                    1020 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1021 group (post-fader sends)
                        1022 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
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
