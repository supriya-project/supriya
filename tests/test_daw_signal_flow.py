import time

from uqbar.strings import normalize

from supriya.daw import Application, DCDevice


def test_01():
    application = Application()
    application.boot()
    track_one = application.add_track(name="one")
    track_one.devices.append(DCDevice(dc=0.5))
    track_two = application.add_track(name="two")
    track_one.add_send(track_two)
    time.sleep(0.25)
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
                        1023 group (dcdevice)
                            1024 27824b3521efd98dfc575933e04a111f
                                active: 1.0, dc: 0.5, gate: 1.0, lag: 0.1, out: 26.0
                    1019 group (pre-fader sends)
                    1020 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1021 group (post-fader sends)
                        1022 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                        1032 mixer/send/2x2 (to two)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 30.0
                1025 group (two)
                    1026 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1027 group (device container)
                    1028 group (pre-fader sends)
                    1029 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1030 group (post-fader sends)
                        1031 mixer/send/2x2 (to master track)
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
    assert track_one._levels == {
        "input": ([0.0, 0.0], [0.0, 0.0]),
        "postfader": ([0.5, 0.5], [0.5, 0.5]),
        "prefader": ([0.5, 0.5], [0.5, 0.5]),
    }
    assert track_two._levels == {
        "input": ([0.5, 0.5], [0.5, 0.5]),
        "postfader": ([0.5, 0.5], [0.5, 0.5]),
        "prefader": ([0.5, 0.5], [0.5, 0.5]),
    }
    assert application.master_track._levels == {
        "input": ([1.0, 1.0], [1.0, 1.0]),
        "postfader": ([1.0, 1.0], [1.0, 1.0]),
        "prefader": ([1.0, 1.0], [1.0, 1.0]),
    }


def test_02():
    application = Application()
    application.boot()
    track_one = application.add_track(name="one")
    track_two = application.add_track(name="two")
    track_two.devices.append(DCDevice(dc=0.5))
    track_two.add_send(track_one)
    time.sleep(0.25)
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
                    1020 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1021 group (post-fader sends)
                        1022 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1023 group (two)
                    1024 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1025 group (device container)
                        1030 group (dcdevice)
                            1031 27824b3521efd98dfc575933e04a111f
                                active: 1.0, dc: 0.5, gate: 1.0, lag: 0.1, out: 30.0
                    1026 group (pre-fader sends)
                    1027 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1028 group (post-fader sends)
                        1029 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
                        1032 mixer/send/2x2 (to one)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 24.0
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
    assert track_one._levels == {
        "input": ([0.5, 0.5], [0.5, 0.5]),
        "postfader": ([0.5, 0.5], [0.5, 0.5]),
        "prefader": ([0.5, 0.5], [0.5, 0.5]),
    }
    assert track_two._levels == {
        "input": ([0.0, 0.0], [0.0, 0.0]),
        "postfader": ([0.5, 0.5], [0.5, 0.5]),
        "prefader": ([0.5, 0.5], [0.5, 0.5]),
    }
    assert application.master_track._levels == {
        "input": ([1.0, 1.0], [1.0, 1.0]),
        "postfader": ([1.0, 1.0], [1.0, 1.0]),
        "prefader": ([1.0, 1.0], [1.0, 1.0]),
    }
