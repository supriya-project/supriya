from uqbar.strings import normalize


def test_dc_index_synthdef_factory(dc_index_synthdef_factory):
    synthdef = dc_index_synthdef_factory.build(name="test")
    assert normalize(str(synthdef)) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.ir: null
            -   Control.kr: null
            -   BinaryOpUGen(EQUAL).kr/0:
                    left: Control.kr[0:index]
                    right: 0.0
            -   BinaryOpUGen(EQUAL).kr/1:
                    left: Control.kr[0:index]
                    right: 1.0
            -   DC.ar:
                    source: 1.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: DC.ar[0]
                    right: BinaryOpUGen(EQUAL).kr/0[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: DC.ar[0]
                    right: BinaryOpUGen(EQUAL).kr/1[0]
            -   Out.ar:
                    bus: Control.ir[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
        """
    )


def test_track_mute_solo_application(track_mute_solo_application):
    track_mute_solo_application.boot()
    assert str(track_mute_solo_application.primary_context.query()) == normalize(
        """
        NODE TREE 1000 group (Context)
            1001 group (Tracks)
                1002 group (a)
                    1003 group (Parameters)
                    1010 group (Receives)
                    1004 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 24.0
                    1009 group (SubTracks)
                    1005 mixer/levels/8 (InputLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1011 group (Devices)
                        1012 group (AudioEffect)
                            1016 mixer/patch[replace]/8x8 (DeviceIn)
                                active: 1.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 32.0
                            1013 group (Parameters)
                            1014 group (Body)
                                1015 7e3d216f841357d2a2e2ab2c3415df6f
                                    out: 32.0, index: 0.0
                            1017 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 32.0, lag: 0.01, mix: 1.0, out: 24.0
                    1006 mixer/levels/8 (PrefaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1018 group (PreFaderSends)
                    1007 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, out: 24.0
                    1019 group (PostFaderSends)
                        1163 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 216.0
                    1008 mixer/levels/8 (PostfaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                1020 group (b)
                    1021 group (Parameters)
                    1066 group (Receives)
                    1022 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.01, out: 48.0
                    1027 group (SubTracks)
                        1028 group (ba)
                            1029 group (Parameters)
                            1036 group (Receives)
                            1030 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 56.0, lag: 0.01, out: 64.0
                            1035 group (SubTracks)
                            1031 mixer/levels/8 (InputLevels)
                                out: 64.0, gate: 1.0, lag: 0.01
                            1037 group (Devices)
                                1038 group (AudioEffect)
                                    1042 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 72.0
                                    1039 group (Parameters)
                                    1040 group (Body)
                                        1041 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 72.0, index: 2.0
                                    1043 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 72.0, lag: 0.01, mix: 1.0, out: 64.0
                            1032 mixer/levels/8 (PrefaderLevels)
                                out: 64.0, gate: 1.0, lag: 0.01
                            1044 group (PreFaderSends)
                            1033 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 64.0, lag: 0.01, out: 64.0
                            1045 group (PostFaderSends)
                                1046 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 48.0
                            1034 mixer/levels/8 (PostfaderLevels)
                                out: 64.0, gate: 1.0, lag: 0.01
                        1047 group (bb)
                            1048 group (Parameters)
                            1055 group (Receives)
                            1049 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 80.0, lag: 0.01, out: 88.0
                            1054 group (SubTracks)
                            1050 mixer/levels/8 (InputLevels)
                                out: 88.0, gate: 1.0, lag: 0.01
                            1056 group (Devices)
                                1057 group (AudioEffect)
                                    1061 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 88.0, lag: 0.01, out: 96.0
                                    1058 group (Parameters)
                                    1059 group (Body)
                                        1060 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 96.0, index: 3.0
                                    1062 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 96.0, lag: 0.01, mix: 1.0, out: 88.0
                            1051 mixer/levels/8 (PrefaderLevels)
                                out: 88.0, gate: 1.0, lag: 0.01
                            1063 group (PreFaderSends)
                            1052 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 88.0, lag: 0.01, out: 88.0
                            1064 group (PostFaderSends)
                                1065 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 88.0, lag: 0.01, out: 48.0
                            1053 mixer/levels/8 (PostfaderLevels)
                                out: 88.0, gate: 1.0, lag: 0.01
                    1023 mixer/levels/8 (InputLevels)
                        out: 48.0, gate: 1.0, lag: 0.01
                    1067 group (Devices)
                        1068 group (AudioEffect)
                            1072 mixer/patch[replace]/8x8 (DeviceIn)
                                active: 1.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 104.0
                            1069 group (Parameters)
                            1070 group (Body)
                                1071 7e3d216f841357d2a2e2ab2c3415df6f
                                    out: 104.0, index: 1.0
                            1073 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 104.0, lag: 0.01, mix: 1.0, out: 48.0
                    1024 mixer/levels/8 (PrefaderLevels)
                        out: 48.0, gate: 1.0, lag: 0.01
                    1074 group (PreFaderSends)
                    1025 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 48.0, lag: 0.01, out: 48.0
                    1075 group (PostFaderSends)
                        1164 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 216.0
                    1026 mixer/levels/8 (PostfaderLevels)
                        out: 48.0, gate: 1.0, lag: 0.01
                1076 group (c)
                    1077 group (Parameters)
                    1141 group (Receives)
                    1078 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 112.0, lag: 0.01, out: 120.0
                    1083 group (SubTracks)
                        1084 group (ca)
                            1085 group (Parameters)
                            1092 group (Receives)
                            1086 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 128.0, lag: 0.01, out: 136.0
                            1091 group (SubTracks)
                            1087 mixer/levels/8 (InputLevels)
                                out: 136.0, gate: 1.0, lag: 0.01
                            1093 group (Devices)
                                1094 group (AudioEffect)
                                    1098 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 136.0, lag: 0.01, out: 144.0
                                    1095 group (Parameters)
                                    1096 group (Body)
                                        1097 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 144.0, index: 5.0
                                    1099 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 144.0, lag: 0.01, mix: 1.0, out: 136.0
                            1088 mixer/levels/8 (PrefaderLevels)
                                out: 136.0, gate: 1.0, lag: 0.01
                            1100 group (PreFaderSends)
                            1089 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 136.0, lag: 0.01, out: 136.0
                            1101 group (PostFaderSends)
                                1102 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 136.0, lag: 0.01, out: 120.0
                            1090 mixer/levels/8 (PostfaderLevels)
                                out: 136.0, gate: 1.0, lag: 0.01
                        1103 group (cb)
                            1104 group (Parameters)
                            1130 group (Receives)
                            1105 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 152.0, lag: 0.01, out: 160.0
                            1110 group (SubTracks)
                                1111 group (cba)
                                    1112 group (Parameters)
                                    1119 group (Receives)
                                    1113 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 168.0, lag: 0.01, out: 176.0
                                    1118 group (SubTracks)
                                    1114 mixer/levels/8 (InputLevels)
                                        out: 176.0, gate: 1.0, lag: 0.01
                                    1120 group (Devices)
                                        1121 group (AudioEffect)
                                            1125 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 176.0, lag: 0.01, out: 184.0
                                            1122 group (Parameters)
                                            1123 group (Body)
                                                1124 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 184.0, index: 7.0
                                            1126 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 184.0, lag: 0.01, mix: 1.0, out: 176.0
                                    1115 mixer/levels/8 (PrefaderLevels)
                                        out: 176.0, gate: 1.0, lag: 0.01
                                    1127 group (PreFaderSends)
                                    1116 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 176.0, lag: 0.01, out: 176.0
                                    1128 group (PostFaderSends)
                                        1129 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 176.0, lag: 0.01, out: 160.0
                                    1117 mixer/levels/8 (PostfaderLevels)
                                        out: 176.0, gate: 1.0, lag: 0.01
                            1106 mixer/levels/8 (InputLevels)
                                out: 160.0, gate: 1.0, lag: 0.01
                            1131 group (Devices)
                                1132 group (AudioEffect)
                                    1136 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 192.0
                                    1133 group (Parameters)
                                    1134 group (Body)
                                        1135 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 192.0, index: 6.0
                                    1137 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 192.0, lag: 0.01, mix: 1.0, out: 160.0
                            1107 mixer/levels/8 (PrefaderLevels)
                                out: 160.0, gate: 1.0, lag: 0.01
                            1138 group (PreFaderSends)
                            1108 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 160.0, lag: 0.01, out: 160.0
                            1139 group (PostFaderSends)
                                1140 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 120.0
                            1109 mixer/levels/8 (PostfaderLevels)
                                out: 160.0, gate: 1.0, lag: 0.01
                    1079 mixer/levels/8 (InputLevels)
                        out: 120.0, gate: 1.0, lag: 0.01
                    1142 group (Devices)
                        1143 group (AudioEffect)
                            1147 mixer/patch[replace]/8x8 (DeviceIn)
                                active: 1.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 200.0
                            1144 group (Parameters)
                            1145 group (Body)
                                1146 7e3d216f841357d2a2e2ab2c3415df6f
                                    out: 200.0, index: 4.0
                            1148 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 200.0, lag: 0.01, mix: 1.0, out: 120.0
                    1080 mixer/levels/8 (PrefaderLevels)
                        out: 120.0, gate: 1.0, lag: 0.01
                    1149 group (PreFaderSends)
                    1081 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 120.0, lag: 0.01, out: 120.0
                    1150 group (PostFaderSends)
                        1165 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 216.0
                    1082 mixer/levels/8 (PostfaderLevels)
                        out: 120.0, gate: 1.0, lag: 0.01
            1151 group (MasterTrack)
                1152 group (Parameters)
                1158 group (Receives)
                1153 mixer/patch[fb,gain]/8x8 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 208.0, lag: 0.01, out: 216.0
                1154 mixer/levels/8 (InputLevels)
                    out: 216.0, gate: 1.0, lag: 0.01
                1159 group (Devices)
                1155 mixer/levels/8 (PrefaderLevels)
                    out: 216.0, gate: 1.0, lag: 0.01
                1160 group (PreFaderSends)
                1156 mixer/patch[gain,hard,replace]/8x8 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 216.0, lag: 0.01, out: 216.0
                1161 group (PostFaderSends)
                    1162 mixer/patch/8x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 216.0, lag: 0.01, out: 0.0
                1157 mixer/levels/8 (PostfaderLevels)
                    out: 216.0, gate: 1.0, lag: 0.01
            1166 group (CueTrack)
                1167 group (Parameters)
                1173 group (Receives)
                1168 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 224.0, lag: 0.01, out: 226.0
                1169 mixer/levels/2 (InputLevels)
                    out: 226.0, gate: 1.0, lag: 0.01
                1174 group (Devices)
                1170 mixer/levels/2 (PrefaderLevels)
                    out: 226.0, gate: 1.0, lag: 0.01
                1175 group (PreFaderSends)
                1171 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 226.0, lag: 0.01, out: 226.0
                1176 group (PostFaderSends)
                    1177 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 226.0, lag: 0.01, out: 2.0
                1172 mixer/levels/2 (PostfaderLevels)
                    out: 226.0, gate: 1.0, lag: 0.01
        """
    )


def test_channel_count_application(channel_count_application):
    channel_count_application.boot()
    assert str(channel_count_application.primary_context.query()) == normalize(
        """
        NODE TREE 1000 group (Context)
            1001 group (Tracks)
                1002 group (One)
                    1003 group (Parameters)
                    1010 group (Receives)
                    1004 mixer/patch[fb,gain]/2x2 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
                    1009 group (SubTracks)
                    1005 mixer/levels/2 (InputLevels)
                        out: 18.0, gate: 1.0, lag: 0.01
                    1011 group (Devices)
                        1012 group (Rack)
                            1013 mixer/patch[gain]/2x2 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 20.0
                            1015 group (ChainContainer)
                                1016 group (Chain)
                                    1017 group (Parameters)
                                    1023 group (Receives)
                                    1018 mixer/patch[fb,gain]/2x2 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 22.0, lag: 0.01, out: 24.0
                                    1019 mixer/levels/2 (InputLevels)
                                        out: 24.0, gate: 1.0, lag: 0.01
                                    1024 group (Devices)
                                        1025 group (Device)
                                            1029 mixer/patch[replace]/2x2 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 26.0
                                            1026 group (Parameters)
                                            1027 group (Body)
                                                1028 ab5b942cf898e9d22891fff080fee99e
                                                    out: 26.0, index: 0.0
                                            1030 mixer/patch[hard,mix]/2x2 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 26.0, lag: 0.01, mix: 1.0, out: 24.0
                                    1020 mixer/levels/2 (PrefaderLevels)
                                        out: 24.0, gate: 1.0, lag: 0.01
                                    1031 group (PreFaderSends)
                                    1021 mixer/patch[gain,hard,replace]/2x2 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, out: 24.0
                                    1032 group (PostFaderSends)
                                        1033 mixer/patch[gain]/2x2 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 20.0
                                    1022 mixer/levels/2 (PostfaderLevels)
                                        out: 24.0, gate: 1.0, lag: 0.01
                            1014 mixer/patch[hard,mix]/2x2 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 20.0, lag: 0.01, mix: 1.0, out: 18.0
                    1006 mixer/levels/2 (PrefaderLevels)
                        out: 18.0, gate: 1.0, lag: 0.01
                    1034 group (PreFaderSends)
                    1007 mixer/patch[gain,hard,replace]/2x2 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
                    1035 group (PostFaderSends)
                        1073 mixer/patch[gain]/2x2 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 38.0
                    1008 mixer/levels/2 (PostfaderLevels)
                        out: 18.0, gate: 1.0, lag: 0.01
                1036 group (Two)
                    1037 group (Parameters)
                    1057 group (Receives)
                    1038 mixer/patch[fb,gain]/2x2 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.01, out: 30.0
                    1043 group (SubTracks)
                        1044 group (Three)
                            1045 group (Parameters)
                            1052 group (Receives)
                            1046 mixer/patch[fb,gain]/2x2 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.01, out: 34.0
                            1051 group (SubTracks)
                            1047 mixer/levels/2 (InputLevels)
                                out: 34.0, gate: 1.0, lag: 0.01
                            1053 group (Devices)
                            1048 mixer/levels/2 (PrefaderLevels)
                                out: 34.0, gate: 1.0, lag: 0.01
                            1054 group (PreFaderSends)
                            1049 mixer/patch[gain,hard,replace]/2x2 (Output)
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 34.0, lag: 0.01, out: 34.0
                            1055 group (PostFaderSends)
                                1056 mixer/patch[gain]/2x2 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.01, out: 30.0
                            1050 mixer/levels/2 (PostfaderLevels)
                                out: 34.0, gate: 1.0, lag: 0.01
                    1039 mixer/levels/2 (InputLevels)
                        out: 30.0, gate: 1.0, lag: 0.01
                    1058 group (Devices)
                    1040 mixer/levels/2 (PrefaderLevels)
                        out: 30.0, gate: 1.0, lag: 0.01
                    1059 group (PreFaderSends)
                    1041 mixer/patch[gain,hard,replace]/2x2 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 30.0, lag: 0.01, out: 30.0
                    1060 group (PostFaderSends)
                        1074 mixer/patch[gain]/2x2 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.01, out: 38.0
                    1042 mixer/levels/2 (PostfaderLevels)
                        out: 30.0, gate: 1.0, lag: 0.01
            1061 group (MasterTrack)
                1062 group (Parameters)
                1068 group (Receives)
                1063 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.01, out: 38.0
                1064 mixer/levels/2 (InputLevels)
                    out: 38.0, gate: 1.0, lag: 0.01
                1069 group (Devices)
                1065 mixer/levels/2 (PrefaderLevels)
                    out: 38.0, gate: 1.0, lag: 0.01
                1070 group (PreFaderSends)
                1066 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 38.0, lag: 0.01, out: 38.0
                1071 group (PostFaderSends)
                    1072 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 38.0, lag: 0.01, out: 0.0
                1067 mixer/levels/2 (PostfaderLevels)
                    out: 38.0, gate: 1.0, lag: 0.01
            1075 group (CueTrack)
                1076 group (Parameters)
                1082 group (Receives)
                1077 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.01, out: 42.0
                1078 mixer/levels/2 (InputLevels)
                    out: 42.0, gate: 1.0, lag: 0.01
                1083 group (Devices)
                1079 mixer/levels/2 (PrefaderLevels)
                    out: 42.0, gate: 1.0, lag: 0.01
                1084 group (PreFaderSends)
                1080 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 42.0, lag: 0.01, out: 42.0
                1085 group (PostFaderSends)
                    1086 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 42.0, lag: 0.01, out: 2.0
                1081 mixer/levels/2 (PostfaderLevels)
                    out: 42.0, gate: 1.0, lag: 0.01
        """
    )


def test_chain_mute_solo_application(chain_mute_solo_application):
    chain_mute_solo_application.boot()
    assert str(chain_mute_solo_application.primary_context.query()) == normalize(
        """
        NODE TREE 1000 group (Context)
            1001 group (Tracks)
                1002 group (Track)
                    1003 group (Parameters)
                    1010 group (Receives)
                    1004 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 24.0
                    1009 group (SubTracks)
                    1005 mixer/levels/8 (InputLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1011 group (Devices)
                        1012 group (outer/a)
                            1013 mixer/patch[gain]/8x8 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 32.0
                            1015 group (ChainContainer)
                                1016 group (outer/a/a)
                                    1017 group (Parameters)
                                    1023 group (Receives)
                                    1018 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.01, out: 48.0
                                    1019 mixer/levels/8 (InputLevels)
                                        out: 48.0, gate: 1.0, lag: 0.01
                                    1024 group (Devices)
                                        1025 group (AudioEffect)
                                            1029 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 56.0
                                            1026 group (Parameters)
                                            1027 group (Body)
                                                1028 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 56.0, index: 0.0
                                            1030 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 56.0, lag: 0.01, mix: 1.0, out: 48.0
                                    1020 mixer/levels/8 (PrefaderLevels)
                                        out: 48.0, gate: 1.0, lag: 0.01
                                    1031 group (PreFaderSends)
                                    1021 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 48.0, lag: 0.01, out: 48.0
                                    1032 group (PostFaderSends)
                                        1033 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 32.0
                                    1022 mixer/levels/8 (PostfaderLevels)
                                        out: 48.0, gate: 1.0, lag: 0.01
                                1034 group (outer/a/b)
                                    1035 group (Parameters)
                                    1041 group (Receives)
                                    1036 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 72.0
                                    1037 mixer/levels/8 (InputLevels)
                                        out: 72.0, gate: 1.0, lag: 0.01
                                    1042 group (Devices)
                                        1043 group (inner/a)
                                            1044 mixer/patch[gain]/8x8 (RackIn)
                                                active: 1.0, gain: 0.0, gate: 1.0, in_: 72.0, lag: 0.01, out: 80.0
                                            1046 group (ChainContainer)
                                                1047 group (inner/a/a)
                                                    1048 group (Parameters)
                                                    1054 group (Receives)
                                                    1049 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 88.0, lag: 0.01, out: 96.0
                                                    1050 mixer/levels/8 (InputLevels)
                                                        out: 96.0, gate: 1.0, lag: 0.01
                                                    1055 group (Devices)
                                                        1056 group (AudioEffect)
                                                            1060 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 96.0, lag: 0.01, out: 104.0
                                                            1057 group (Parameters)
                                                            1058 group (Body)
                                                                1059 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 104.0, index: 2.0
                                                            1061 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 104.0, lag: 0.01, mix: 1.0, out: 96.0
                                                    1051 mixer/levels/8 (PrefaderLevels)
                                                        out: 96.0, gate: 1.0, lag: 0.01
                                                    1062 group (PreFaderSends)
                                                    1052 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 96.0, lag: 0.01, out: 96.0
                                                    1063 group (PostFaderSends)
                                                        1064 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 96.0, lag: 0.01, out: 80.0
                                                    1053 mixer/levels/8 (PostfaderLevels)
                                                        out: 96.0, gate: 1.0, lag: 0.01
                                                1065 group (inner/a/b)
                                                    1066 group (Parameters)
                                                    1072 group (Receives)
                                                    1067 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 112.0, lag: 0.01, out: 120.0
                                                    1068 mixer/levels/8 (InputLevels)
                                                        out: 120.0, gate: 1.0, lag: 0.01
                                                    1073 group (Devices)
                                                        1074 group (AudioEffect)
                                                            1078 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 128.0
                                                            1075 group (Parameters)
                                                            1076 group (Body)
                                                                1077 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 128.0, index: 3.0
                                                            1079 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 128.0, lag: 0.01, mix: 1.0, out: 120.0
                                                    1069 mixer/levels/8 (PrefaderLevels)
                                                        out: 120.0, gate: 1.0, lag: 0.01
                                                    1080 group (PreFaderSends)
                                                    1070 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 120.0, lag: 0.01, out: 120.0
                                                    1081 group (PostFaderSends)
                                                        1082 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 80.0
                                                    1071 mixer/levels/8 (PostfaderLevels)
                                                        out: 120.0, gate: 1.0, lag: 0.01
                                            1045 mixer/patch[hard,mix]/8x8 (RackOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 80.0, lag: 0.01, mix: 1.0, out: 72.0
                                        1083 group (AudioEffect)
                                            1087 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 72.0, lag: 0.01, out: 136.0
                                            1084 group (Parameters)
                                            1085 group (Body)
                                                1086 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 136.0, index: 1.0
                                            1088 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 136.0, lag: 0.01, mix: 1.0, out: 72.0
                                    1038 mixer/levels/8 (PrefaderLevels)
                                        out: 72.0, gate: 1.0, lag: 0.01
                                    1089 group (PreFaderSends)
                                    1039 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 72.0, lag: 0.01, out: 72.0
                                    1090 group (PostFaderSends)
                                        1091 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 72.0, lag: 0.01, out: 32.0
                                    1040 mixer/levels/8 (PostfaderLevels)
                                        out: 72.0, gate: 1.0, lag: 0.01
                            1014 mixer/patch[hard,mix]/8x8 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 32.0, lag: 0.01, mix: 1.0, out: 24.0
                        1092 group (outer/b)
                            1093 mixer/patch[gain]/8x8 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 144.0
                            1095 group (ChainContainer)
                                1096 group (outer/b/a)
                                    1097 group (Parameters)
                                    1103 group (Receives)
                                    1098 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 152.0, lag: 0.01, out: 160.0
                                    1099 mixer/levels/8 (InputLevels)
                                        out: 160.0, gate: 1.0, lag: 0.01
                                    1104 group (Devices)
                                        1105 group (AudioEffect)
                                            1109 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 168.0
                                            1106 group (Parameters)
                                            1107 group (Body)
                                                1108 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 168.0, index: 4.0
                                            1110 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 168.0, lag: 0.01, mix: 1.0, out: 160.0
                                    1100 mixer/levels/8 (PrefaderLevels)
                                        out: 160.0, gate: 1.0, lag: 0.01
                                    1111 group (PreFaderSends)
                                    1101 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 160.0, lag: 0.01, out: 160.0
                                    1112 group (PostFaderSends)
                                        1113 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 144.0
                                    1102 mixer/levels/8 (PostfaderLevels)
                                        out: 160.0, gate: 1.0, lag: 0.01
                                1114 group (outer/b/b)
                                    1115 group (Parameters)
                                    1121 group (Receives)
                                    1116 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 176.0, lag: 0.01, out: 184.0
                                    1117 mixer/levels/8 (InputLevels)
                                        out: 184.0, gate: 1.0, lag: 0.01
                                    1122 group (Devices)
                                        1123 group (inner/b)
                                            1124 mixer/patch[gain]/8x8 (RackIn)
                                                active: 1.0, gain: 0.0, gate: 1.0, in_: 184.0, lag: 0.01, out: 192.0
                                            1126 group (ChainContainer)
                                                1127 group (inner/b/a)
                                                    1128 group (Parameters)
                                                    1134 group (Receives)
                                                    1129 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 200.0, lag: 0.01, out: 208.0
                                                    1130 mixer/levels/8 (InputLevels)
                                                        out: 208.0, gate: 1.0, lag: 0.01
                                                    1135 group (Devices)
                                                        1136 group (AudioEffect)
                                                            1140 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 208.0, lag: 0.01, out: 216.0
                                                            1137 group (Parameters)
                                                            1138 group (Body)
                                                                1139 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 216.0, index: 6.0
                                                            1141 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 216.0, lag: 0.01, mix: 1.0, out: 208.0
                                                    1131 mixer/levels/8 (PrefaderLevels)
                                                        out: 208.0, gate: 1.0, lag: 0.01
                                                    1142 group (PreFaderSends)
                                                    1132 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 208.0, lag: 0.01, out: 208.0
                                                    1143 group (PostFaderSends)
                                                        1144 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 208.0, lag: 0.01, out: 192.0
                                                    1133 mixer/levels/8 (PostfaderLevels)
                                                        out: 208.0, gate: 1.0, lag: 0.01
                                                1145 group (inner/b/b)
                                                    1146 group (Parameters)
                                                    1152 group (Receives)
                                                    1147 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 224.0, lag: 0.01, out: 232.0
                                                    1148 mixer/levels/8 (InputLevels)
                                                        out: 232.0, gate: 1.0, lag: 0.01
                                                    1153 group (Devices)
                                                        1154 group (AudioEffect)
                                                            1158 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 232.0, lag: 0.01, out: 240.0
                                                            1155 group (Parameters)
                                                            1156 group (Body)
                                                                1157 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 240.0, index: 7.0
                                                            1159 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 240.0, lag: 0.01, mix: 1.0, out: 232.0
                                                    1149 mixer/levels/8 (PrefaderLevels)
                                                        out: 232.0, gate: 1.0, lag: 0.01
                                                    1160 group (PreFaderSends)
                                                    1150 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 232.0, lag: 0.01, out: 232.0
                                                    1161 group (PostFaderSends)
                                                        1162 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 232.0, lag: 0.01, out: 192.0
                                                    1151 mixer/levels/8 (PostfaderLevels)
                                                        out: 232.0, gate: 1.0, lag: 0.01
                                            1125 mixer/patch[hard,mix]/8x8 (RackOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 192.0, lag: 0.01, mix: 1.0, out: 184.0
                                        1163 group (AudioEffect)
                                            1167 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 184.0, lag: 0.01, out: 248.0
                                            1164 group (Parameters)
                                            1165 group (Body)
                                                1166 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 248.0, index: 5.0
                                            1168 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 248.0, lag: 0.01, mix: 1.0, out: 184.0
                                    1118 mixer/levels/8 (PrefaderLevels)
                                        out: 184.0, gate: 1.0, lag: 0.01
                                    1169 group (PreFaderSends)
                                    1119 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 184.0, lag: 0.01, out: 184.0
                                    1170 group (PostFaderSends)
                                        1171 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 184.0, lag: 0.01, out: 144.0
                                    1120 mixer/levels/8 (PostfaderLevels)
                                        out: 184.0, gate: 1.0, lag: 0.01
                            1094 mixer/patch[hard,mix]/8x8 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 144.0, lag: 0.01, mix: 1.0, out: 24.0
                    1006 mixer/levels/8 (PrefaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1172 group (PreFaderSends)
                    1007 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, out: 24.0
                    1173 group (PostFaderSends)
                        1186 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 264.0
                    1008 mixer/levels/8 (PostfaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
            1174 group (MasterTrack)
                1175 group (Parameters)
                1181 group (Receives)
                1176 mixer/patch[fb,gain]/8x8 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 256.0, lag: 0.01, out: 264.0
                1177 mixer/levels/8 (InputLevels)
                    out: 264.0, gate: 1.0, lag: 0.01
                1182 group (Devices)
                1178 mixer/levels/8 (PrefaderLevels)
                    out: 264.0, gate: 1.0, lag: 0.01
                1183 group (PreFaderSends)
                1179 mixer/patch[gain,hard,replace]/8x8 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 264.0, lag: 0.01, out: 264.0
                1184 group (PostFaderSends)
                    1185 mixer/patch/8x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 264.0, lag: 0.01, out: 0.0
                1180 mixer/levels/8 (PostfaderLevels)
                    out: 264.0, gate: 1.0, lag: 0.01
            1187 group (CueTrack)
                1188 group (Parameters)
                1194 group (Receives)
                1189 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 272.0, lag: 0.01, out: 274.0
                1190 mixer/levels/2 (InputLevels)
                    out: 274.0, gate: 1.0, lag: 0.01
                1195 group (Devices)
                1191 mixer/levels/2 (PrefaderLevels)
                    out: 274.0, gate: 1.0, lag: 0.01
                1196 group (PreFaderSends)
                1192 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 274.0, lag: 0.01, out: 274.0
                1197 group (PostFaderSends)
                    1198 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 274.0, lag: 0.01, out: 2.0
                1193 mixer/levels/2 (PostfaderLevels)
                    out: 274.0, gate: 1.0, lag: 0.01
        """
    )
