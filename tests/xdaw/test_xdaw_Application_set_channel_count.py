import time

from uqbar.strings import normalize

from supriya.xdaw import Action, Allocatable, Parameter


def test_channel_count(channel_count_application):
    items = [channel_count_application]
    items.extend(
        x
        for x in channel_count_application.depth_first()
        if not isinstance(x, (Action, Parameter)) and x.name
    )
    assert {
        x.name: (x.channel_count, x.effective_channel_count) for x in items[1:]
    } == {
        "Chain": (None, 2),
        "Context": (None, 2),
        "Device": (None, 2),
        "One": (None, 2),
        "Rack": (None, 2),
        "Three": (None, 2),
        "Two": (None, 2),
    }
    channel_count_application.set_channel_count(4)
    assert {
        x.name: (x.channel_count, x.effective_channel_count) for x in items[1:]
    } == {
        "Chain": (None, 4),
        "Context": (None, 4),
        "Device": (None, 4),
        "One": (None, 4),
        "Rack": (None, 4),
        "Three": (None, 4),
        "Two": (None, 4),
    }


def test_audio_buses(channel_count_application):
    for node in channel_count_application.depth_first(prototype=Allocatable):
        for audio_bus_proxy in node.audio_bus_proxies.values():
            assert audio_bus_proxy.channel_count == node.effective_channel_count
    channel_count_application.set_channel_count(4)
    for node in channel_count_application.depth_first(prototype=Allocatable):
        for audio_bus_proxy in node.audio_bus_proxies.values():
            assert audio_bus_proxy.channel_count == node.effective_channel_count


def test_levels(channel_count_application):
    channel_count_application.boot()
    master_levels = channel_count_application.primary_context.master_track.rms_levels
    track_levels = channel_count_application.primary_context["One"].rms_levels
    time.sleep(0.2)
    assert [round(x, 2) for x in track_levels["postfader"]] == [1.0, 0.0]
    assert [round(x, 2) for x in master_levels["input"]] == [1.0, 0.0]
    channel_count_application.set_channel_count(4)
    time.sleep(0.2)
    assert [round(x, 2) for x in track_levels["postfader"]] == [1.0, 0.0, 0.0, 0.0]
    assert [round(x, 2) for x in master_levels["input"]] == [1.0, 0.0, 0.0, 0.0]


def test_query(channel_count_application):
    context = channel_count_application["Context"]
    channel_count_application.boot()
    with context.provider.server.osc_io.capture() as transcript:
        channel_count_application.set_channel_count(4)
    time.sleep(0.1)
    assert len(transcript.sent_messages) == 1
    after = str(context.query())
    assert after == normalize(
        """
        NODE TREE 1000 group (Context)
            1001 group (Tracks)
                1002 group (One)
                    1009 group (Parameters)
                        1010 group (gain)
                        1011 group (panning)
                    1012 group (Receives)
                    1098 mixer/patch[fb,gain]/4x4 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 44.0
                    1008 group (SubTracks)
                    1099 mixer/levels/4 (InputLevels)
                        out: 44.0, gate: 1.0, lag: 0.01
                    1013 group (Devices)
                        1014 group (Rack)
                            1103 mixer/patch[gain]/4x4 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.01, out: 48.0
                            1017 group (ChainContainer)
                                1018 group (Chain)
                                    1024 group (Parameters)
                                        1025 group (gain)
                                        1026 group (panning)
                                    1027 group (Receives)
                                    1105 mixer/patch[fb,gain]/4x4 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.01, out: 52.0
                                    1106 mixer/levels/4 (InputLevels)
                                        out: 52.0, gate: 1.0, lag: 0.01
                                    1028 group (Devices)
                                        1029 group (Device)
                                            1111 mixer/patch[replace]/4x4 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 52.0, lag: 0.01, out: 24.0
                                            1030 group (Parameters)
                                            1031 group (Body)
                                                1110 15a77f27cd96f4488c4a9b094478d045
                                                    out: 24.0, index: 0.0
                                            1112 mixer/patch[hard,mix]/4x4 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, mix: 1.0, out: 52.0
                                    1107 mixer/levels/4 (PrefaderLevels)
                                        out: 52.0, gate: 1.0, lag: 0.01
                                    1035 group (PreFaderSends)
                                    1108 mixer/patch[gain,hard,replace]/4x4 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 52.0, lag: 0.01, out: 52.0
                                    1036 group (PostFaderSends)
                                        1113 mixer/patch[gain]/4x4 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 52.0, lag: 0.01, out: 48.0
                                    1109 mixer/levels/4 (PostfaderLevels)
                                        out: 52.0, gate: 1.0, lag: 0.01
                            1104 mixer/patch[hard,mix]/4x4 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 48.0, lag: 0.01, mix: 1.0, out: 44.0
                    1100 mixer/levels/4 (PrefaderLevels)
                        out: 44.0, gate: 1.0, lag: 0.01
                    1038 group (PreFaderSends)
                    1101 mixer/patch[gain,hard,replace]/4x4 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 44.0, lag: 0.01, out: 44.0
                    1039 group (PostFaderSends)
                        1133 mixer/patch[gain]/4x4 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.01, out: 64.0
                    1102 mixer/levels/4 (PostfaderLevels)
                        out: 44.0, gate: 1.0, lag: 0.01
                1040 group (Two)
                    1062 group (Parameters)
                        1063 group (gain)
                        1064 group (panning)
                    1065 group (Receives)
                    1115 mixer/patch[fb,gain]/4x4 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.01, out: 56.0
                    1046 group (SubTracks)
                        1047 group (Three)
                            1054 group (Parameters)
                                1055 group (gain)
                                1056 group (panning)
                            1057 group (Receives)
                            1120 mixer/patch[fb,gain]/4x4 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.01, out: 60.0
                            1053 group (SubTracks)
                            1121 mixer/levels/4 (InputLevels)
                                out: 60.0, gate: 1.0, lag: 0.01
                            1058 group (Devices)
                            1122 mixer/levels/4 (PrefaderLevels)
                                out: 60.0, gate: 1.0, lag: 0.01
                            1059 group (PreFaderSends)
                            1123 mixer/patch[gain,hard,replace]/4x4 (Output)
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 60.0, lag: 0.01, out: 60.0
                            1060 group (PostFaderSends)
                                1125 mixer/patch[gain]/4x4 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 60.0, lag: 0.01, out: 56.0
                            1124 mixer/levels/4 (PostfaderLevels)
                                out: 60.0, gate: 1.0, lag: 0.01
                    1116 mixer/levels/4 (InputLevels)
                        out: 56.0, gate: 1.0, lag: 0.01
                    1066 group (Devices)
                    1117 mixer/levels/4 (PrefaderLevels)
                        out: 56.0, gate: 1.0, lag: 0.01
                    1067 group (PreFaderSends)
                    1118 mixer/patch[gain,hard,replace]/4x4 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 56.0, lag: 0.01, out: 56.0
                    1068 group (PostFaderSends)
                        1134 mixer/patch[gain]/4x4 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 56.0, lag: 0.01, out: 64.0
                    1119 mixer/levels/4 (PostfaderLevels)
                        out: 56.0, gate: 1.0, lag: 0.01
            1069 group (MasterTrack)
                1075 group (Parameters)
                    1076 group (gain)
                1077 group (Receives)
                1127 mixer/patch[fb,gain]/4x4 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.01, out: 64.0
                1128 mixer/levels/4 (InputLevels)
                    out: 64.0, gate: 1.0, lag: 0.01
                1078 group (Devices)
                1129 mixer/levels/4 (PrefaderLevels)
                    out: 64.0, gate: 1.0, lag: 0.01
                1079 group (PreFaderSends)
                1130 mixer/patch[gain,hard,replace]/4x4 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 64.0, lag: 0.01, out: 64.0
                1080 group (PostFaderSends)
                    1132 mixer/patch/4x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 0.0
                1131 mixer/levels/4 (PostfaderLevels)
                    out: 64.0, gate: 1.0, lag: 0.01
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
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 42.0, lag: 0.01, out: 42.0
                1096 group (PostFaderSends)
                    1097 mixer/patch/2x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 42.0, lag: 0.01, out: 2.0
                1089 mixer/levels/2 (PostfaderLevels)
                    out: 42.0, gate: 1.0, lag: 0.01
        """
    )
