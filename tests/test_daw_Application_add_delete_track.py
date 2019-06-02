from uqbar.strings import normalize

from supriya import Server
from supriya.daw import Application, Track


def test_01():
    server = Server.default()

    application = Application()
    assert application.server is None
    assert str(application.node) == normalize(
        """
        ??? group (application)
            ??? transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            ??? group (track container)
            ??? group (return track container)
            ??? group (master track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 0.0, lag: 0.1, out: 0.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 0.0
                ??? group (post-fader sends)
            ??? group (cue track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 0.0, lag: 0.1, out: 0.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 0.0
                ??? group (post-fader sends)
    """
    )

    track_one = application.add_track()
    assert isinstance(track_one, Track)
    assert track_one.application is application
    assert track_one.server is None
    assert track_one.graph_order == (1, 0)
    assert str(application.node) == normalize(
        """
        ??? group (application)
            ??? transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            ??? group (track container)
                ??? group (track)
                    ??? mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 0.0, lag: 0.1, out: 0.0
                    ??? group (device container)
                    ??? group (pre-fader sends)
                    ??? mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 0.0
                    ??? group (post-fader sends)
            ??? group (return track container)
            ??? group (master track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 0.0, lag: 0.1, out: 0.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 0.0
                ??? group (post-fader sends)
            ??? group (cue track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 0.0, lag: 0.1, out: 0.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 0.0
                ??? group (post-fader sends)
        """
    )

    application.boot()
    assert server.is_running
    assert application.server is server
    assert track_one.server is server
    assert str(application.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1003 group (track)
                    1004 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1005 group (device container)
                    1006 group (pre-fader sends)
                    1007 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1008 group (post-fader sends)
                        1022 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
            1009 group (return track container)
            1010 group (master track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1015 group (post-fader sends)
            1016 group (cue track)
                1017 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1018 group (device container)
                1019 group (pre-fader sends)
                1020 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1021 group (post-fader sends)
        """
    )

    track_two = application.add_track()
    assert isinstance(track_two, Track)
    assert track_two.application is application
    assert track_two.graph_order == (1, 1)
    assert track_two.server is server
    assert str(application.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1003 group (track)
                    1004 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1005 group (device container)
                    1006 group (pre-fader sends)
                    1007 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1008 group (post-fader sends)
                        1022 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1023 group (track)
                    1024 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1025 group (device container)
                    1026 group (pre-fader sends)
                    1027 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1028 group (post-fader sends)
                        1029 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
            1009 group (return track container)
            1010 group (master track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1015 group (post-fader sends)
            1016 group (cue track)
                1017 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1018 group (device container)
                1019 group (pre-fader sends)
                1020 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1021 group (post-fader sends)
        """
    )

    track_one.delete()
    assert track_one.application is None
    assert track_one.server is None
    assert str(application.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1023 group (track)
                    1024 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    1025 group (device container)
                    1026 group (pre-fader sends)
                    1027 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    1028 group (post-fader sends)
                        1029 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 22.0
            1009 group (return track container)
            1010 group (master track)
                1011 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1012 group (device container)
                1013 group (pre-fader sends)
                1014 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1015 group (post-fader sends)
            1016 group (cue track)
                1017 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1018 group (device container)
                1019 group (pre-fader sends)
                1020 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1021 group (post-fader sends)
        """
    )
    assert str(track_one.node) == normalize(
        """
        ??? group (track)
            ??? mixer/track-input/2
                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
            ??? group (device container)
            ??? group (pre-fader sends)
            ??? mixer/track-output/2
                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
            ??? group (post-fader sends)
        """
    )

    application.quit()
    assert application.server is None
    assert track_one.application is None
    assert track_two.application is application
    assert track_one.server is None
    assert track_two.server is None
    assert str(application.node) == normalize(
        """
        ??? group (application)
            ??? transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            ??? group (track container)
                ??? group (track)
                    ??? mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                    ??? group (device container)
                    ??? group (pre-fader sends)
                    ??? mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                    ??? group (post-fader sends)
            ??? group (return track container)
            ??? group (master track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                ??? group (post-fader sends)
            ??? group (cue track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                ??? group (post-fader sends)
    """
    )

    track_two.delete()
    assert track_two.application is None
    assert track_two.server is None
    assert str(application.node) == normalize(
        """
        ??? group (application)
            ??? transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            ??? group (track container)
            ??? group (return track container)
            ??? group (master track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                ??? group (post-fader sends)
            ??? group (cue track)
                ??? mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                ??? group (device container)
                ??? group (pre-fader sends)
                ??? mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                ??? group (post-fader sends)
        """
    )
    assert str(track_two.node) == normalize(
        """
        ??? group (track)
            ??? mixer/track-input/2
                active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
            ??? group (device container)
            ??? group (pre-fader sends)
            ??? mixer/track-output/2
                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
            ??? group (post-fader sends)
        """
    )
