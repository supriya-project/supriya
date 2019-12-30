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
                    1009 group (Parameters)
                        1010 group (gain)
                        1011 group (panning)
                    1012 group (Receives)
                    1003 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 24.0
                    1008 group (SubTracks)
                    1004 mixer/levels/8 (InputLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1013 group (Devices)
                        1014 group (AudioEffect)
                            1018 mixer/patch[replace]/8x8 (DeviceIn)
                                active: 1.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 32.0
                            1015 group (Parameters)
                            1016 group (Body)
                                1017 7e3d216f841357d2a2e2ab2c3415df6f
                                    out: 32.0, index: 0.0
                            1019 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 32.0, lag: 0.01, mix: 1.0, out: 24.0
                    1005 mixer/levels/8 (PrefaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1020 group (PreFaderSends)
                    1006 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: c0, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, out: 24.0
                    1021 group (PostFaderSends)
                        1180 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 216.0
                    1007 mixer/levels/8 (PostfaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                1022 group (b)
                    1071 group (Parameters)
                        1072 group (gain)
                        1073 group (panning)
                    1074 group (Receives)
                    1023 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.01, out: 48.0
                    1028 group (SubTracks)
                        1029 group (ba)
                            1036 group (Parameters)
                                1037 group (gain)
                                1038 group (panning)
                            1039 group (Receives)
                            1030 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 56.0, lag: 0.01, out: 64.0
                            1035 group (SubTracks)
                            1031 mixer/levels/8 (InputLevels)
                                out: 64.0, gate: 1.0, lag: 0.01
                            1040 group (Devices)
                                1041 group (AudioEffect)
                                    1045 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 72.0
                                    1042 group (Parameters)
                                    1043 group (Body)
                                        1044 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 72.0, index: 2.0
                                    1046 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 72.0, lag: 0.01, mix: 1.0, out: 64.0
                            1032 mixer/levels/8 (PrefaderLevels)
                                out: 64.0, gate: 1.0, lag: 0.01
                            1047 group (PreFaderSends)
                            1033 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: c4, gate: 1.0, hard_gate: 1.0, in_: 64.0, lag: 0.01, out: 64.0
                            1048 group (PostFaderSends)
                                1049 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 48.0
                            1034 mixer/levels/8 (PostfaderLevels)
                                out: 64.0, gate: 1.0, lag: 0.01
                        1050 group (bb)
                            1057 group (Parameters)
                                1058 group (gain)
                                1059 group (panning)
                            1060 group (Receives)
                            1051 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 80.0, lag: 0.01, out: 88.0
                            1056 group (SubTracks)
                            1052 mixer/levels/8 (InputLevels)
                                out: 88.0, gate: 1.0, lag: 0.01
                            1061 group (Devices)
                                1062 group (AudioEffect)
                                    1066 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 88.0, lag: 0.01, out: 96.0
                                    1063 group (Parameters)
                                    1064 group (Body)
                                        1065 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 96.0, index: 3.0
                                    1067 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 96.0, lag: 0.01, mix: 1.0, out: 88.0
                            1053 mixer/levels/8 (PrefaderLevels)
                                out: 88.0, gate: 1.0, lag: 0.01
                            1068 group (PreFaderSends)
                            1054 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: c6, gate: 1.0, hard_gate: 1.0, in_: 88.0, lag: 0.01, out: 88.0
                            1069 group (PostFaderSends)
                                1070 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 88.0, lag: 0.01, out: 48.0
                            1055 mixer/levels/8 (PostfaderLevels)
                                out: 88.0, gate: 1.0, lag: 0.01
                    1024 mixer/levels/8 (InputLevels)
                        out: 48.0, gate: 1.0, lag: 0.01
                    1075 group (Devices)
                        1076 group (AudioEffect)
                            1080 mixer/patch[replace]/8x8 (DeviceIn)
                                active: 1.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 104.0
                            1077 group (Parameters)
                            1078 group (Body)
                                1079 7e3d216f841357d2a2e2ab2c3415df6f
                                    out: 104.0, index: 1.0
                            1081 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 104.0, lag: 0.01, mix: 1.0, out: 48.0
                    1025 mixer/levels/8 (PrefaderLevels)
                        out: 48.0, gate: 1.0, lag: 0.01
                    1082 group (PreFaderSends)
                    1026 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: c2, gate: 1.0, hard_gate: 1.0, in_: 48.0, lag: 0.01, out: 48.0
                    1083 group (PostFaderSends)
                        1181 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 216.0
                    1027 mixer/levels/8 (PostfaderLevels)
                        out: 48.0, gate: 1.0, lag: 0.01
                1084 group (c)
                    1154 group (Parameters)
                        1155 group (gain)
                        1156 group (panning)
                    1157 group (Receives)
                    1085 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 112.0, lag: 0.01, out: 120.0
                    1090 group (SubTracks)
                        1091 group (ca)
                            1098 group (Parameters)
                                1099 group (gain)
                                1100 group (panning)
                            1101 group (Receives)
                            1092 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 128.0, lag: 0.01, out: 136.0
                            1097 group (SubTracks)
                            1093 mixer/levels/8 (InputLevels)
                                out: 136.0, gate: 1.0, lag: 0.01
                            1102 group (Devices)
                                1103 group (AudioEffect)
                                    1107 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 136.0, lag: 0.01, out: 144.0
                                    1104 group (Parameters)
                                    1105 group (Body)
                                        1106 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 144.0, index: 5.0
                                    1108 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 144.0, lag: 0.01, mix: 1.0, out: 136.0
                            1094 mixer/levels/8 (PrefaderLevels)
                                out: 136.0, gate: 1.0, lag: 0.01
                            1109 group (PreFaderSends)
                            1095 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: c10, gate: 1.0, hard_gate: 1.0, in_: 136.0, lag: 0.01, out: 136.0
                            1110 group (PostFaderSends)
                                1111 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 136.0, lag: 0.01, out: 120.0
                            1096 mixer/levels/8 (PostfaderLevels)
                                out: 136.0, gate: 1.0, lag: 0.01
                        1112 group (cb)
                            1140 group (Parameters)
                                1141 group (gain)
                                1142 group (panning)
                            1143 group (Receives)
                            1113 mixer/patch[fb,gain]/8x8 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 152.0, lag: 0.01, out: 160.0
                            1118 group (SubTracks)
                                1119 group (cba)
                                    1126 group (Parameters)
                                        1127 group (gain)
                                        1128 group (panning)
                                    1129 group (Receives)
                                    1120 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 168.0, lag: 0.01, out: 176.0
                                    1125 group (SubTracks)
                                    1121 mixer/levels/8 (InputLevels)
                                        out: 176.0, gate: 1.0, lag: 0.01
                                    1130 group (Devices)
                                        1131 group (AudioEffect)
                                            1135 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 176.0, lag: 0.01, out: 184.0
                                            1132 group (Parameters)
                                            1133 group (Body)
                                                1134 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 184.0, index: 7.0
                                            1136 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 184.0, lag: 0.01, mix: 1.0, out: 176.0
                                    1122 mixer/levels/8 (PrefaderLevels)
                                        out: 176.0, gate: 1.0, lag: 0.01
                                    1137 group (PreFaderSends)
                                    1123 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: c14, gate: 1.0, hard_gate: 1.0, in_: 176.0, lag: 0.01, out: 176.0
                                    1138 group (PostFaderSends)
                                        1139 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 176.0, lag: 0.01, out: 160.0
                                    1124 mixer/levels/8 (PostfaderLevels)
                                        out: 176.0, gate: 1.0, lag: 0.01
                            1114 mixer/levels/8 (InputLevels)
                                out: 160.0, gate: 1.0, lag: 0.01
                            1144 group (Devices)
                                1145 group (AudioEffect)
                                    1149 mixer/patch[replace]/8x8 (DeviceIn)
                                        active: 1.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 192.0
                                    1146 group (Parameters)
                                    1147 group (Body)
                                        1148 7e3d216f841357d2a2e2ab2c3415df6f
                                            out: 192.0, index: 6.0
                                    1150 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                        active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 192.0, lag: 0.01, mix: 1.0, out: 160.0
                            1115 mixer/levels/8 (PrefaderLevels)
                                out: 160.0, gate: 1.0, lag: 0.01
                            1151 group (PreFaderSends)
                            1116 mixer/patch[gain,hard,replace]/8x8 (Output)
                                active: 1.0, gain: c12, gate: 1.0, hard_gate: 1.0, in_: 160.0, lag: 0.01, out: 160.0
                            1152 group (PostFaderSends)
                                1153 mixer/patch[gain]/8x8 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 120.0
                            1117 mixer/levels/8 (PostfaderLevels)
                                out: 160.0, gate: 1.0, lag: 0.01
                    1086 mixer/levels/8 (InputLevels)
                        out: 120.0, gate: 1.0, lag: 0.01
                    1158 group (Devices)
                        1159 group (AudioEffect)
                            1163 mixer/patch[replace]/8x8 (DeviceIn)
                                active: 1.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 200.0
                            1160 group (Parameters)
                            1161 group (Body)
                                1162 7e3d216f841357d2a2e2ab2c3415df6f
                                    out: 200.0, index: 4.0
                            1164 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 200.0, lag: 0.01, mix: 1.0, out: 120.0
                    1087 mixer/levels/8 (PrefaderLevels)
                        out: 120.0, gate: 1.0, lag: 0.01
                    1165 group (PreFaderSends)
                    1088 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: c8, gate: 1.0, hard_gate: 1.0, in_: 120.0, lag: 0.01, out: 120.0
                    1166 group (PostFaderSends)
                        1182 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 216.0
                    1089 mixer/levels/8 (PostfaderLevels)
                        out: 120.0, gate: 1.0, lag: 0.01
            1167 group (MasterTrack)
                1173 group (Parameters)
                    1174 group (gain)
                1175 group (Receives)
                1168 mixer/patch[fb,gain]/8x8 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 208.0, lag: 0.01, out: 216.0
                1169 mixer/levels/8 (InputLevels)
                    out: 216.0, gate: 1.0, lag: 0.01
                1176 group (Devices)
                1170 mixer/levels/8 (PrefaderLevels)
                    out: 216.0, gate: 1.0, lag: 0.01
                1177 group (PreFaderSends)
                1171 mixer/patch[gain,hard,replace]/8x8 (Output)
                    active: 1.0, gain: c16, gate: 1.0, hard_gate: 1.0, in_: 216.0, lag: 0.01, out: 216.0
                1178 group (PostFaderSends)
                    1179 mixer/patch/8x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 216.0, lag: 0.01, out: 0.0
                1172 mixer/levels/8 (PostfaderLevels)
                    out: 216.0, gate: 1.0, lag: 0.01
            1183 group (CueTrack)
                1189 group (Parameters)
                    1190 group (gain)
                    1191 group (mix)
                1192 group (Receives)
                1184 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 224.0, lag: 0.01, out: 226.0
                1185 mixer/levels/2 (InputLevels)
                    out: 226.0, gate: 1.0, lag: 0.01
                1193 group (Devices)
                1186 mixer/levels/2 (PrefaderLevels)
                    out: 226.0, gate: 1.0, lag: 0.01
                1194 group (PreFaderSends)
                1187 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: c17, gate: 1.0, hard_gate: 1.0, in_: 226.0, lag: 0.01, out: 226.0
                1195 group (PostFaderSends)
                    1196 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 226.0, lag: 0.01, out: 2.0
                1188 mixer/levels/2 (PostfaderLevels)
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
                    1009 group (Parameters)
                        1010 group (gain)
                        1011 group (panning)
                    1012 group (Receives)
                    1003 mixer/patch[fb,gain]/2x2 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 18.0
                    1008 group (SubTracks)
                    1004 mixer/levels/2 (InputLevels)
                        out: 18.0, gate: 1.0, lag: 0.01
                    1013 group (Devices)
                        1014 group (Rack)
                            1015 mixer/patch[gain]/2x2 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 20.0
                            1017 group (ChainContainer)
                                1018 group (Chain)
                                    1024 group (Parameters)
                                        1025 group (gain)
                                        1026 group (panning)
                                    1027 group (Receives)
                                    1019 mixer/patch[fb,gain]/2x2 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 22.0, lag: 0.01, out: 24.0
                                    1020 mixer/levels/2 (InputLevels)
                                        out: 24.0, gate: 1.0, lag: 0.01
                                    1028 group (Devices)
                                        1029 group (Device)
                                            1033 mixer/patch[replace]/2x2 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 26.0
                                            1030 group (Parameters)
                                            1031 group (Body)
                                                1032 ab5b942cf898e9d22891fff080fee99e
                                                    out: 26.0, index: 0.0
                                            1034 mixer/patch[hard,mix]/2x2 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 26.0, lag: 0.01, mix: 1.0, out: 24.0
                                    1021 mixer/levels/2 (PrefaderLevels)
                                        out: 24.0, gate: 1.0, lag: 0.01
                                    1035 group (PreFaderSends)
                                    1022 mixer/patch[gain,hard,replace]/2x2 (Output)
                                        active: 1.0, gain: c2, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, out: 24.0
                                    1036 group (PostFaderSends)
                                        1037 mixer/patch[gain]/2x2 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 20.0
                                    1023 mixer/levels/2 (PostfaderLevels)
                                        out: 24.0, gate: 1.0, lag: 0.01
                            1016 mixer/patch[hard,mix]/2x2 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 20.0, lag: 0.01, mix: 1.0, out: 18.0
                    1005 mixer/levels/2 (PrefaderLevels)
                        out: 18.0, gate: 1.0, lag: 0.01
                    1038 group (PreFaderSends)
                    1006 mixer/patch[gain,hard,replace]/2x2 (Output)
                        active: 1.0, gain: c0, gate: 1.0, hard_gate: 1.0, in_: 18.0, lag: 0.01, out: 18.0
                    1039 group (PostFaderSends)
                        1082 mixer/patch[gain]/2x2 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 18.0, lag: 0.01, out: 38.0
                    1007 mixer/levels/2 (PostfaderLevels)
                        out: 18.0, gate: 1.0, lag: 0.01
                1040 group (Two)
                    1062 group (Parameters)
                        1063 group (gain)
                        1064 group (panning)
                    1065 group (Receives)
                    1041 mixer/patch[fb,gain]/2x2 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.01, out: 30.0
                    1046 group (SubTracks)
                        1047 group (Three)
                            1054 group (Parameters)
                                1055 group (gain)
                                1056 group (panning)
                            1057 group (Receives)
                            1048 mixer/patch[fb,gain]/2x2 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.01, out: 34.0
                            1053 group (SubTracks)
                            1049 mixer/levels/2 (InputLevels)
                                out: 34.0, gate: 1.0, lag: 0.01
                            1058 group (Devices)
                            1050 mixer/levels/2 (PrefaderLevels)
                                out: 34.0, gate: 1.0, lag: 0.01
                            1059 group (PreFaderSends)
                            1051 mixer/patch[gain,hard,replace]/2x2 (Output)
                                active: 1.0, gain: c6, gate: 1.0, hard_gate: 1.0, in_: 34.0, lag: 0.01, out: 34.0
                            1060 group (PostFaderSends)
                                1061 mixer/patch[gain]/2x2 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.01, out: 30.0
                            1052 mixer/levels/2 (PostfaderLevels)
                                out: 34.0, gate: 1.0, lag: 0.01
                    1042 mixer/levels/2 (InputLevels)
                        out: 30.0, gate: 1.0, lag: 0.01
                    1066 group (Devices)
                    1043 mixer/levels/2 (PrefaderLevels)
                        out: 30.0, gate: 1.0, lag: 0.01
                    1067 group (PreFaderSends)
                    1044 mixer/patch[gain,hard,replace]/2x2 (Output)
                        active: 1.0, gain: c4, gate: 1.0, hard_gate: 1.0, in_: 30.0, lag: 0.01, out: 30.0
                    1068 group (PostFaderSends)
                        1083 mixer/patch[gain]/2x2 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.01, out: 38.0
                    1045 mixer/levels/2 (PostfaderLevels)
                        out: 30.0, gate: 1.0, lag: 0.01
            1069 group (MasterTrack)
                1075 group (Parameters)
                    1076 group (gain)
                1077 group (Receives)
                1070 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.01, out: 38.0
                1071 mixer/levels/2 (InputLevels)
                    out: 38.0, gate: 1.0, lag: 0.01
                1078 group (Devices)
                1072 mixer/levels/2 (PrefaderLevels)
                    out: 38.0, gate: 1.0, lag: 0.01
                1079 group (PreFaderSends)
                1073 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: c8, gate: 1.0, hard_gate: 1.0, in_: 38.0, lag: 0.01, out: 38.0
                1080 group (PostFaderSends)
                    1081 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 38.0, lag: 0.01, out: 0.0
                1074 mixer/levels/2 (PostfaderLevels)
                    out: 38.0, gate: 1.0, lag: 0.01
            1084 group (CueTrack)
                1090 group (Parameters)
                    1091 group (gain)
                    1092 group (mix)
                1093 group (Receives)
                1085 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.01, out: 42.0
                1086 mixer/levels/2 (InputLevels)
                    out: 42.0, gate: 1.0, lag: 0.01
                1094 group (Devices)
                1087 mixer/levels/2 (PrefaderLevels)
                    out: 42.0, gate: 1.0, lag: 0.01
                1095 group (PreFaderSends)
                1088 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: c9, gate: 1.0, hard_gate: 1.0, in_: 42.0, lag: 0.01, out: 42.0
                1096 group (PostFaderSends)
                    1097 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 42.0, lag: 0.01, out: 2.0
                1089 mixer/levels/2 (PostfaderLevels)
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
                    1009 group (Parameters)
                        1010 group (gain)
                        1011 group (panning)
                    1012 group (Receives)
                    1003 mixer/patch[fb,gain]/8x8 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 24.0
                    1008 group (SubTracks)
                    1004 mixer/levels/8 (InputLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1013 group (Devices)
                        1014 group (outer/a)
                            1015 mixer/patch[gain]/8x8 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 32.0
                            1017 group (ChainContainer)
                                1018 group (outer/a/a)
                                    1024 group (Parameters)
                                        1025 group (gain)
                                        1026 group (panning)
                                    1027 group (Receives)
                                    1019 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.01, out: 48.0
                                    1020 mixer/levels/8 (InputLevels)
                                        out: 48.0, gate: 1.0, lag: 0.01
                                    1028 group (Devices)
                                        1029 group (AudioEffect)
                                            1033 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 56.0
                                            1030 group (Parameters)
                                            1031 group (Body)
                                                1032 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 56.0, index: 0.0
                                            1034 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 56.0, lag: 0.01, mix: 1.0, out: 48.0
                                    1021 mixer/levels/8 (PrefaderLevels)
                                        out: 48.0, gate: 1.0, lag: 0.01
                                    1035 group (PreFaderSends)
                                    1022 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: c2, gate: 1.0, hard_gate: 1.0, in_: 48.0, lag: 0.01, out: 48.0
                                    1036 group (PostFaderSends)
                                        1037 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 48.0, lag: 0.01, out: 32.0
                                    1023 mixer/levels/8 (PostfaderLevels)
                                        out: 48.0, gate: 1.0, lag: 0.01
                                1038 group (outer/a/b)
                                    1044 group (Parameters)
                                        1045 group (gain)
                                        1046 group (panning)
                                    1047 group (Receives)
                                    1039 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 72.0
                                    1040 mixer/levels/8 (InputLevels)
                                        out: 72.0, gate: 1.0, lag: 0.01
                                    1048 group (Devices)
                                        1049 group (inner/a)
                                            1050 mixer/patch[gain]/8x8 (RackIn)
                                                active: 1.0, gain: 0.0, gate: 1.0, in_: 72.0, lag: 0.01, out: 80.0
                                            1052 group (ChainContainer)
                                                1053 group (inner/a/a)
                                                    1059 group (Parameters)
                                                        1060 group (gain)
                                                        1061 group (panning)
                                                    1062 group (Receives)
                                                    1054 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 88.0, lag: 0.01, out: 96.0
                                                    1055 mixer/levels/8 (InputLevels)
                                                        out: 96.0, gate: 1.0, lag: 0.01
                                                    1063 group (Devices)
                                                        1064 group (AudioEffect)
                                                            1068 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 96.0, lag: 0.01, out: 104.0
                                                            1065 group (Parameters)
                                                            1066 group (Body)
                                                                1067 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 104.0, index: 2.0
                                                            1069 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 104.0, lag: 0.01, mix: 1.0, out: 96.0
                                                    1056 mixer/levels/8 (PrefaderLevels)
                                                        out: 96.0, gate: 1.0, lag: 0.01
                                                    1070 group (PreFaderSends)
                                                    1057 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: c6, gate: 1.0, hard_gate: 1.0, in_: 96.0, lag: 0.01, out: 96.0
                                                    1071 group (PostFaderSends)
                                                        1072 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 96.0, lag: 0.01, out: 80.0
                                                    1058 mixer/levels/8 (PostfaderLevels)
                                                        out: 96.0, gate: 1.0, lag: 0.01
                                                1073 group (inner/a/b)
                                                    1079 group (Parameters)
                                                        1080 group (gain)
                                                        1081 group (panning)
                                                    1082 group (Receives)
                                                    1074 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 112.0, lag: 0.01, out: 120.0
                                                    1075 mixer/levels/8 (InputLevels)
                                                        out: 120.0, gate: 1.0, lag: 0.01
                                                    1083 group (Devices)
                                                        1084 group (AudioEffect)
                                                            1088 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 128.0
                                                            1085 group (Parameters)
                                                            1086 group (Body)
                                                                1087 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 128.0, index: 3.0
                                                            1089 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 128.0, lag: 0.01, mix: 1.0, out: 120.0
                                                    1076 mixer/levels/8 (PrefaderLevels)
                                                        out: 120.0, gate: 1.0, lag: 0.01
                                                    1090 group (PreFaderSends)
                                                    1077 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: c8, gate: 1.0, hard_gate: 1.0, in_: 120.0, lag: 0.01, out: 120.0
                                                    1091 group (PostFaderSends)
                                                        1092 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 120.0, lag: 0.01, out: 80.0
                                                    1078 mixer/levels/8 (PostfaderLevels)
                                                        out: 120.0, gate: 1.0, lag: 0.01
                                            1051 mixer/patch[hard,mix]/8x8 (RackOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 80.0, lag: 0.01, mix: 1.0, out: 72.0
                                        1093 group (AudioEffect)
                                            1097 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 72.0, lag: 0.01, out: 136.0
                                            1094 group (Parameters)
                                            1095 group (Body)
                                                1096 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 136.0, index: 1.0
                                            1098 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 136.0, lag: 0.01, mix: 1.0, out: 72.0
                                    1041 mixer/levels/8 (PrefaderLevels)
                                        out: 72.0, gate: 1.0, lag: 0.01
                                    1099 group (PreFaderSends)
                                    1042 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: c4, gate: 1.0, hard_gate: 1.0, in_: 72.0, lag: 0.01, out: 72.0
                                    1100 group (PostFaderSends)
                                        1101 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 72.0, lag: 0.01, out: 32.0
                                    1043 mixer/levels/8 (PostfaderLevels)
                                        out: 72.0, gate: 1.0, lag: 0.01
                            1016 mixer/patch[hard,mix]/8x8 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 32.0, lag: 0.01, mix: 1.0, out: 24.0
                        1102 group (outer/b)
                            1103 mixer/patch[gain]/8x8 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 144.0
                            1105 group (ChainContainer)
                                1106 group (outer/b/a)
                                    1112 group (Parameters)
                                        1113 group (gain)
                                        1114 group (panning)
                                    1115 group (Receives)
                                    1107 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 152.0, lag: 0.01, out: 160.0
                                    1108 mixer/levels/8 (InputLevels)
                                        out: 160.0, gate: 1.0, lag: 0.01
                                    1116 group (Devices)
                                        1117 group (AudioEffect)
                                            1121 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 168.0
                                            1118 group (Parameters)
                                            1119 group (Body)
                                                1120 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 168.0, index: 4.0
                                            1122 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 168.0, lag: 0.01, mix: 1.0, out: 160.0
                                    1109 mixer/levels/8 (PrefaderLevels)
                                        out: 160.0, gate: 1.0, lag: 0.01
                                    1123 group (PreFaderSends)
                                    1110 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: c10, gate: 1.0, hard_gate: 1.0, in_: 160.0, lag: 0.01, out: 160.0
                                    1124 group (PostFaderSends)
                                        1125 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 160.0, lag: 0.01, out: 144.0
                                    1111 mixer/levels/8 (PostfaderLevels)
                                        out: 160.0, gate: 1.0, lag: 0.01
                                1126 group (outer/b/b)
                                    1132 group (Parameters)
                                        1133 group (gain)
                                        1134 group (panning)
                                    1135 group (Receives)
                                    1127 mixer/patch[fb,gain]/8x8 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 176.0, lag: 0.01, out: 184.0
                                    1128 mixer/levels/8 (InputLevels)
                                        out: 184.0, gate: 1.0, lag: 0.01
                                    1136 group (Devices)
                                        1137 group (inner/b)
                                            1138 mixer/patch[gain]/8x8 (RackIn)
                                                active: 1.0, gain: 0.0, gate: 1.0, in_: 184.0, lag: 0.01, out: 192.0
                                            1140 group (ChainContainer)
                                                1141 group (inner/b/a)
                                                    1147 group (Parameters)
                                                        1148 group (gain)
                                                        1149 group (panning)
                                                    1150 group (Receives)
                                                    1142 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 200.0, lag: 0.01, out: 208.0
                                                    1143 mixer/levels/8 (InputLevels)
                                                        out: 208.0, gate: 1.0, lag: 0.01
                                                    1151 group (Devices)
                                                        1152 group (AudioEffect)
                                                            1156 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 208.0, lag: 0.01, out: 216.0
                                                            1153 group (Parameters)
                                                            1154 group (Body)
                                                                1155 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 216.0, index: 6.0
                                                            1157 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 216.0, lag: 0.01, mix: 1.0, out: 208.0
                                                    1144 mixer/levels/8 (PrefaderLevels)
                                                        out: 208.0, gate: 1.0, lag: 0.01
                                                    1158 group (PreFaderSends)
                                                    1145 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: c14, gate: 1.0, hard_gate: 1.0, in_: 208.0, lag: 0.01, out: 208.0
                                                    1159 group (PostFaderSends)
                                                        1160 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 208.0, lag: 0.01, out: 192.0
                                                    1146 mixer/levels/8 (PostfaderLevels)
                                                        out: 208.0, gate: 1.0, lag: 0.01
                                                1161 group (inner/b/b)
                                                    1167 group (Parameters)
                                                        1168 group (gain)
                                                        1169 group (panning)
                                                    1170 group (Receives)
                                                    1162 mixer/patch[fb,gain]/8x8 (Input)
                                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 224.0, lag: 0.01, out: 232.0
                                                    1163 mixer/levels/8 (InputLevels)
                                                        out: 232.0, gate: 1.0, lag: 0.01
                                                    1171 group (Devices)
                                                        1172 group (AudioEffect)
                                                            1176 mixer/patch[replace]/8x8 (DeviceIn)
                                                                active: 1.0, gate: 1.0, in_: 232.0, lag: 0.01, out: 240.0
                                                            1173 group (Parameters)
                                                            1174 group (Body)
                                                                1175 7e3d216f841357d2a2e2ab2c3415df6f
                                                                    out: 240.0, index: 7.0
                                                            1177 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 240.0, lag: 0.01, mix: 1.0, out: 232.0
                                                    1164 mixer/levels/8 (PrefaderLevels)
                                                        out: 232.0, gate: 1.0, lag: 0.01
                                                    1178 group (PreFaderSends)
                                                    1165 mixer/patch[gain,hard,replace]/8x8 (Output)
                                                        active: 1.0, gain: c16, gate: 1.0, hard_gate: 1.0, in_: 232.0, lag: 0.01, out: 232.0
                                                    1179 group (PostFaderSends)
                                                        1180 mixer/patch[gain]/8x8 (Send)
                                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 232.0, lag: 0.01, out: 192.0
                                                    1166 mixer/levels/8 (PostfaderLevels)
                                                        out: 232.0, gate: 1.0, lag: 0.01
                                            1139 mixer/patch[hard,mix]/8x8 (RackOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 192.0, lag: 0.01, mix: 1.0, out: 184.0
                                        1181 group (AudioEffect)
                                            1185 mixer/patch[replace]/8x8 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 184.0, lag: 0.01, out: 248.0
                                            1182 group (Parameters)
                                            1183 group (Body)
                                                1184 7e3d216f841357d2a2e2ab2c3415df6f
                                                    out: 248.0, index: 5.0
                                            1186 mixer/patch[hard,mix]/8x8 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 248.0, lag: 0.01, mix: 1.0, out: 184.0
                                    1129 mixer/levels/8 (PrefaderLevels)
                                        out: 184.0, gate: 1.0, lag: 0.01
                                    1187 group (PreFaderSends)
                                    1130 mixer/patch[gain,hard,replace]/8x8 (Output)
                                        active: 1.0, gain: c12, gate: 1.0, hard_gate: 1.0, in_: 184.0, lag: 0.01, out: 184.0
                                    1188 group (PostFaderSends)
                                        1189 mixer/patch[gain]/8x8 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 184.0, lag: 0.01, out: 144.0
                                    1131 mixer/levels/8 (PostfaderLevels)
                                        out: 184.0, gate: 1.0, lag: 0.01
                            1104 mixer/patch[hard,mix]/8x8 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 144.0, lag: 0.01, mix: 1.0, out: 24.0
                    1005 mixer/levels/8 (PrefaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
                    1190 group (PreFaderSends)
                    1006 mixer/patch[gain,hard,replace]/8x8 (Output)
                        active: 1.0, gain: c0, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, out: 24.0
                    1191 group (PostFaderSends)
                        1205 mixer/patch[gain]/8x8 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.01, out: 264.0
                    1007 mixer/levels/8 (PostfaderLevels)
                        out: 24.0, gate: 1.0, lag: 0.01
            1192 group (MasterTrack)
                1198 group (Parameters)
                    1199 group (gain)
                1200 group (Receives)
                1193 mixer/patch[fb,gain]/8x8 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 256.0, lag: 0.01, out: 264.0
                1194 mixer/levels/8 (InputLevels)
                    out: 264.0, gate: 1.0, lag: 0.01
                1201 group (Devices)
                1195 mixer/levels/8 (PrefaderLevels)
                    out: 264.0, gate: 1.0, lag: 0.01
                1202 group (PreFaderSends)
                1196 mixer/patch[gain,hard,replace]/8x8 (Output)
                    active: 1.0, gain: c18, gate: 1.0, hard_gate: 1.0, in_: 264.0, lag: 0.01, out: 264.0
                1203 group (PostFaderSends)
                    1204 mixer/patch/8x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 264.0, lag: 0.01, out: 0.0
                1197 mixer/levels/8 (PostfaderLevels)
                    out: 264.0, gate: 1.0, lag: 0.01
            1206 group (CueTrack)
                1212 group (Parameters)
                    1213 group (gain)
                    1214 group (mix)
                1215 group (Receives)
                1207 mixer/patch[fb,gain]/2x2 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 272.0, lag: 0.01, out: 274.0
                1208 mixer/levels/2 (InputLevels)
                    out: 274.0, gate: 1.0, lag: 0.01
                1216 group (Devices)
                1209 mixer/levels/2 (PrefaderLevels)
                    out: 274.0, gate: 1.0, lag: 0.01
                1217 group (PreFaderSends)
                1210 mixer/patch[gain,hard,replace]/2x2 (Output)
                    active: 1.0, gain: c19, gate: 1.0, hard_gate: 1.0, in_: 274.0, lag: 0.01, out: 274.0
                1218 group (PostFaderSends)
                    1219 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 274.0, lag: 0.01, out: 2.0
                1211 mixer/levels/2 (PostfaderLevels)
                    out: 274.0, gate: 1.0, lag: 0.01
        """
    )
