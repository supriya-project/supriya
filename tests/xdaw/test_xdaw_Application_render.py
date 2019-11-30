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
                            1003 group
                            1010 group
                            1004 mix/patch[fb,gain]/2x2
                            1009 group
                            1005 mixer/levels/2
                            1011 group
                            1006 mixer/levels/2
                            1012 group
                            1007 mix/patch[gain,hard,replace]/2x2
                            1013 group
                                1026 mix/patch[gain]/2x2
                            1008 mixer/levels/2
                    1014 group
                        1015 group
                        1021 group
                        1016 mix/patch[fb,gain]/2x2
                        1017 mixer/levels/2
                        1022 group
                        1018 mixer/levels/2
                        1023 group
                        1019 mix/patch[gain,hard,replace]/2x2
                        1024 group
                            1025 mix/patch/2x2
                        1020 mixer/levels/2
                    1027 group
                        1028 group
                        1034 group
                        1029 mix/patch[fb,gain]/2x2
                        1030 mixer/levels/2
                        1035 group
                        1031 mixer/levels/2
                        1036 group
                        1032 mix/patch[gain,hard,replace]/2x2
                        1037 group
                            1038 mix/patch/2x2
                        1033 mixer/levels/2
        inf:
            NODE TREE 0 group
        """
    )
