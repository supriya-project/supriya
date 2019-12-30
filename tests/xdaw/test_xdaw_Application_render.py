from uqbar.strings import normalize

from supriya.xdaw import Application


def test_1():
    application = Application()
    context = application.add_context()
    context.add_track()
    session = application.render()
    assert application.status == Application.Status.OFFLINE
    assert session.to_strings() == normalize(
        """
        0.0:
            NODE TREE 0 group
                1000 group
                    1001 group
                        1002 group
                            1009 group
                                1010 group
                                1011 group
                            1012 group
                            1003 mixer/patch[fb,gain]/2x2
                            1008 group
                            1004 mixer/levels/2
                            1013 group
                            1005 mixer/levels/2
                            1014 group
                            1006 mixer/patch[gain,hard,replace]/2x2
                            1015 group
                                1029 mixer/patch[gain]/2x2
                            1007 mixer/levels/2
                    1016 group
                        1022 group
                            1023 group
                        1024 group
                        1017 mixer/patch[fb,gain]/2x2
                        1018 mixer/levels/2
                        1025 group
                        1019 mixer/levels/2
                        1026 group
                        1020 mixer/patch[gain,hard,replace]/2x2
                        1027 group
                            1028 mixer/patch/2x2
                        1021 mixer/levels/2
                    1030 group
                        1036 group
                            1037 group
                            1038 group
                        1039 group
                        1031 mixer/patch[fb,gain]/2x2
                        1032 mixer/levels/2
                        1040 group
                        1033 mixer/levels/2
                        1041 group
                        1034 mixer/patch[gain,hard,replace]/2x2
                        1042 group
                            1043 mixer/patch/2x2
                        1035 mixer/levels/2
        inf:
            NODE TREE 0 group
        """
    )
