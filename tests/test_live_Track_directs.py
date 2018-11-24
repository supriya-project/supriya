import time

import uqbar.strings

import supriya.live
import supriya.realtime


def test_01(server):
    server = supriya.realtime.Server().boot()
    mixer = supriya.live.Mixer(channel_count=2, cue_channel_count=1)
    track = mixer.add_track("foo")
    track.add_direct_in([(0, 0), (1, 1)])
    track.add_direct_out([(0, 1), (1, 0)])
    mixer.allocate()
    assert str(server) == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1015 group
                            1022 mixer/direct/0:0,1:1
                                in_: 8.0, out: 22.0, gate: 1.0, lag: 0.1
                            1016 mixer/input/2
                                in_: 22.0, out: 24.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1017 group
                            1018 mixer/send/2x1
                                in_: 24.0, out: 20.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1019 mixer/output/2
                                out: 24.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1020 group
                                1021 mixer/send/2x2
                                    in_: 24.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1023 mixer/direct/0:1,1:0
                                in_: 24.0, out: 0.0, gate: 1.0, lag: 0.1
                    1002 group
                        1003 mixer/input/2
                            in_: 16.0, out: 18.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1004 group
                        1005 mixer/send/2x1
                            in_: 18.0, out: 20.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1006 mixer/output/2
                            out: 18.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                        1007 group
                        1008 mixer/direct/0:0,1:1
                            in_: 18.0, out: 0.0, gate: 1.0, lag: 0.1
                    1009 group
                        1010 mixer/input/1
                            in_: 20.0, out: 21.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1011 group
                        1012 mixer/output/1
                            out: 21.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                        1013 group
                        1014 mixer/direct/0:2
                            in_: 21.0, out: 0.0, gate: 1.0, lag: 0.1
        """
    )
    track.remove_direct_in()
    track.remove_direct_out()
    time.sleep(0.25)
    assert str(server) == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1015 group
                            1016 mixer/input/2
                                in_: 22.0, out: 24.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1017 group
                            1018 mixer/send/2x1
                                in_: 24.0, out: 20.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1019 mixer/output/2
                                out: 24.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1020 group
                                1021 mixer/send/2x2
                                    in_: 24.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                    1002 group
                        1003 mixer/input/2
                            in_: 16.0, out: 18.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1004 group
                        1005 mixer/send/2x1
                            in_: 18.0, out: 20.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1006 mixer/output/2
                            out: 18.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                        1007 group
                        1008 mixer/direct/0:0,1:1
                            in_: 18.0, out: 0.0, gate: 1.0, lag: 0.1
                    1009 group
                        1010 mixer/input/1
                            in_: 20.0, out: 21.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1011 group
                        1012 mixer/output/1
                            out: 21.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                        1013 group
                        1014 mixer/direct/0:2
                            in_: 21.0, out: 0.0, gate: 1.0, lag: 0.1
        """
    )
