import time

import pytest
from uqbar.strings import normalize

from supriya.provider import RealtimeProvider
from supriya.xdaw import Application


def test_error():
    application = Application()
    with pytest.raises(ValueError):
        application.boot()


def test_boot_1():
    application = Application()
    context = application.add_context()
    application.boot()
    time.sleep(0.01)  # wait one cycle because node creation waits on synthdef loading
    assert application.status == Application.Status.REALTIME
    assert isinstance(context.provider, RealtimeProvider)
    assert context.provider.server.is_running
    assert str(context.provider.server) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                    1002 group
                        1003 group
                        1009 group
                        1004 mix/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
                        1005 mixer/levels/2
                            out: 18.0, gate: 1.0, lag: 0.01
                        1010 group
                        1006 mixer/levels/2
                            out: 18.0, gate: 1.0, lag: 0.01
                        1011 group
                        1007 mix/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
                        1012 group
                            1013 mix/patch/2x2
                                active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 0.0
                        1008 mixer/levels/2
                            out: 18.0, gate: 1.0, lag: 0.01
                    1014 group
                        1015 group
                        1021 group
                        1016 mix/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.01, out: 22.0
                        1017 mixer/levels/2
                            out: 22.0, gate: 1.0, lag: 0.01
                        1022 group
                        1018 mixer/levels/2
                            out: 22.0, gate: 1.0, lag: 0.01
                        1023 group
                        1019 mix/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 22.0, lag: 0.01, out: 22.0
                        1024 group
                            1025 mix/patch/2x2
                                active: 1.0, gate: 1.0, in_: 22.0, lag: 0.01, out: 2.0
                        1020 mixer/levels/2
                            out: 22.0, gate: 1.0, lag: 0.01
        """
    )


def test_boot_2():
    application = Application()
    context = application.add_context()
    context.add_track()
    group_track = context.add_track()
    group_track.add_track()
    application.boot()
    time.sleep(0.01)  # wait one cycle because node creation waits on synthdef loading
    assert str(context.provider.server) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1002 group
                            1003 group
                            1010 group
                            1004 mix/patch[fb,gain]/2x2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
                            1009 group
                            1005 mixer/levels/2
                                out: 18.0, gate: 1.0, lag: 0.01
                            1011 group
                            1006 mixer/levels/2
                                out: 18.0, gate: 1.0, lag: 0.01
                            1012 group
                            1007 mix/patch[gain,hard,replace]/2x2
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
                            1013 group
                                1051 mix/patch[gain]/2x2
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 30.0
                            1008 mixer/levels/2
                                out: 18.0, gate: 1.0, lag: 0.01
                        1014 group
                            1015 group
                            1035 group
                            1016 mix/patch[fb,gain]/2x2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.01, out: 22.0
                            1021 group
                                1022 group
                                    1023 group
                                    1030 group
                                    1024 mix/patch[fb,gain]/2x2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 26.0
                                    1029 group
                                    1025 mixer/levels/2
                                        out: 26.0, gate: 1.0, lag: 0.01
                                    1031 group
                                    1026 mixer/levels/2
                                        out: 26.0, gate: 1.0, lag: 0.01
                                    1032 group
                                    1027 mix/patch[gain,hard,replace]/2x2
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 26.0, lag: 0.01, out: 26.0
                                    1033 group
                                        1034 mix/patch[gain]/2x2
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.01, out: 22.0
                                    1028 mixer/levels/2
                                        out: 26.0, gate: 1.0, lag: 0.01
                            1017 mixer/levels/2
                                out: 22.0, gate: 1.0, lag: 0.01
                            1036 group
                            1018 mixer/levels/2
                                out: 22.0, gate: 1.0, lag: 0.01
                            1037 group
                            1019 mix/patch[gain,hard,replace]/2x2
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 22.0, lag: 0.01, out: 22.0
                            1038 group
                                1052 mix/patch[gain]/2x2
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 22.0, lag: 0.01, out: 30.0
                            1020 mixer/levels/2
                                out: 22.0, gate: 1.0, lag: 0.01
                    1039 group
                        1040 group
                        1046 group
                        1041 mix/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.01, out: 30.0
                        1042 mixer/levels/2
                            out: 30.0, gate: 1.0, lag: 0.01
                        1047 group
                        1043 mixer/levels/2
                            out: 30.0, gate: 1.0, lag: 0.01
                        1048 group
                        1044 mix/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 30.0, lag: 0.01, out: 30.0
                        1049 group
                            1050 mix/patch/2x2
                                active: 1.0, gate: 1.0, in_: 30.0, lag: 0.01, out: 0.0
                        1045 mixer/levels/2
                            out: 30.0, gate: 1.0, lag: 0.01
                    1053 group
                        1054 group
                        1060 group
                        1055 mix/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.01, out: 34.0
                        1056 mixer/levels/2
                            out: 34.0, gate: 1.0, lag: 0.01
                        1061 group
                        1057 mixer/levels/2
                            out: 34.0, gate: 1.0, lag: 0.01
                        1062 group
                        1058 mix/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 34.0, lag: 0.01, out: 34.0
                        1063 group
                            1064 mix/patch/2x2
                                active: 1.0, gate: 1.0, in_: 34.0, lag: 0.01, out: 2.0
                        1059 mixer/levels/2
                            out: 34.0, gate: 1.0, lag: 0.01
        """
    )
