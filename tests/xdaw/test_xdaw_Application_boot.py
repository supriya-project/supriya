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
                        1008 group
                            1009 group
                        1010 group
                        1003 mixer/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
                        1004 mixer/levels/2
                            out: 18.0, gate: 1.0, lag: 0.01
                        1011 group
                        1005 mixer/levels/2
                            out: 18.0, gate: 1.0, lag: 0.01
                        1012 group
                        1006 mixer/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: c0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
                        1013 group
                            1014 mixer/patch/2x2
                                active: 1.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 0.0
                        1007 mixer/levels/2
                            out: 18.0, gate: 1.0, lag: 0.01
                    1015 group
                        1021 group
                            1022 group
                            1023 group
                        1024 group
                        1016 mixer/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.01, out: 22.0
                        1017 mixer/levels/2
                            out: 22.0, gate: 1.0, lag: 0.01
                        1025 group
                        1018 mixer/levels/2
                            out: 22.0, gate: 1.0, lag: 0.01
                        1026 group
                        1019 mixer/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: c1, gate: 1.0, hard_gate: 1.0, in_: 22.0, lag: 0.01, out: 22.0
                        1027 group
                            1028 mixer/patch/2x2
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
                            1009 group
                                1010 group
                                1011 group
                            1012 group
                            1003 mixer/patch[fb,gain]/2x2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
                            1008 group
                            1004 mixer/levels/2
                                out: 18.0, gate: 1.0, lag: 0.01
                            1013 group
                            1005 mixer/levels/2
                                out: 18.0, gate: 1.0, lag: 0.01
                            1014 group
                            1006 mixer/patch[gain,hard,replace]/2x2
                                active: 1.0, gain: c0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
                            1015 group
                                1058 mixer/patch[gain]/2x2
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 30.0
                            1007 mixer/levels/2
                                out: 18.0, gate: 1.0, lag: 0.01
                        1016 group
                            1038 group
                                1039 group
                                1040 group
                            1041 group
                            1017 mixer/patch[fb,gain]/2x2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.01, out: 22.0
                            1022 group
                                1023 group
                                    1030 group
                                        1031 group
                                        1032 group
                                    1033 group
                                    1024 mixer/patch[fb,gain]/2x2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 26.0
                                    1029 group
                                    1025 mixer/levels/2
                                        out: 26.0, gate: 1.0, lag: 0.01
                                    1034 group
                                    1026 mixer/levels/2
                                        out: 26.0, gate: 1.0, lag: 0.01
                                    1035 group
                                    1027 mixer/patch[gain,hard,replace]/2x2
                                        active: 1.0, gain: c4, gate: 1.0, hard_gate: 1.0, in_: 26.0, lag: 0.01, out: 26.0
                                    1036 group
                                        1037 mixer/patch[gain]/2x2
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.01, out: 22.0
                                    1028 mixer/levels/2
                                        out: 26.0, gate: 1.0, lag: 0.01
                            1018 mixer/levels/2
                                out: 22.0, gate: 1.0, lag: 0.01
                            1042 group
                            1019 mixer/levels/2
                                out: 22.0, gate: 1.0, lag: 0.01
                            1043 group
                            1020 mixer/patch[gain,hard,replace]/2x2
                                active: 1.0, gain: c2, gate: 1.0, hard_gate: 1.0, in_: 22.0, lag: 0.01, out: 22.0
                            1044 group
                                1059 mixer/patch[gain]/2x2
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 22.0, lag: 0.01, out: 30.0
                            1021 mixer/levels/2
                                out: 22.0, gate: 1.0, lag: 0.01
                    1045 group
                        1051 group
                            1052 group
                        1053 group
                        1046 mixer/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.01, out: 30.0
                        1047 mixer/levels/2
                            out: 30.0, gate: 1.0, lag: 0.01
                        1054 group
                        1048 mixer/levels/2
                            out: 30.0, gate: 1.0, lag: 0.01
                        1055 group
                        1049 mixer/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: c6, gate: 1.0, hard_gate: 1.0, in_: 30.0, lag: 0.01, out: 30.0
                        1056 group
                            1057 mixer/patch/2x2
                                active: 1.0, gate: 1.0, in_: 30.0, lag: 0.01, out: 0.0
                        1050 mixer/levels/2
                            out: 30.0, gate: 1.0, lag: 0.01
                    1060 group
                        1066 group
                            1067 group
                            1068 group
                        1069 group
                        1061 mixer/patch[fb,gain]/2x2
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.01, out: 34.0
                        1062 mixer/levels/2
                            out: 34.0, gate: 1.0, lag: 0.01
                        1070 group
                        1063 mixer/levels/2
                            out: 34.0, gate: 1.0, lag: 0.01
                        1071 group
                        1064 mixer/patch[gain,hard,replace]/2x2
                            active: 1.0, gain: c7, gate: 1.0, hard_gate: 1.0, in_: 34.0, lag: 0.01, out: 34.0
                        1072 group
                            1073 mixer/patch/2x2
                                active: 1.0, gate: 1.0, in_: 34.0, lag: 0.01, out: 2.0
                        1065 mixer/levels/2
                            out: 34.0, gate: 1.0, lag: 0.01
        """
    )
