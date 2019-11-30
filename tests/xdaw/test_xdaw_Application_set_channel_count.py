import time

from uqbar.strings import normalize

from supriya.xdaw import Allocatable


def test_channel_count(channel_count_application):
    items = [channel_count_application]
    items.extend(x for x in channel_count_application.depth_first() if x.name)
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
                    1003 group (Parameters)
                    1010 group (Receives)
                    1087 mixer/patch[fb,gain]/4x4 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.01, out: 44.0
                    1009 group (SubTracks)
                    1088 mixer/levels/4 (InputLevels)
                        out: 44.0, gate: 1.0, lag: 0.01
                    1011 group (Devices)
                        1012 group (Rack)
                            1092 mixer/patch[gain]/4x4 (RackIn)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.01, out: 48.0
                            1015 group (ChainContainer)
                                1016 group (Chain)
                                    1017 group (Parameters)
                                    1023 group (Receives)
                                    1094 mixer/patch[fb,gain]/4x4 (Input)
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.01, out: 52.0
                                    1095 mixer/levels/4 (InputLevels)
                                        out: 52.0, gate: 1.0, lag: 0.01
                                    1024 group (Devices)
                                        1025 group (Device)
                                            1100 mixer/patch[replace]/4x4 (DeviceIn)
                                                active: 1.0, gate: 1.0, in_: 52.0, lag: 0.01, out: 24.0
                                            1026 group (Parameters)
                                            1027 group (Body)
                                                1099 15a77f27cd96f4488c4a9b094478d045
                                                    out: 24.0, index: 0.0
                                            1101 mixer/patch[hard,mix]/4x4 (DeviceOut)
                                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 24.0, lag: 0.01, mix: 1.0, out: 52.0
                                    1096 mixer/levels/4 (PrefaderLevels)
                                        out: 52.0, gate: 1.0, lag: 0.01
                                    1031 group (PreFaderSends)
                                    1097 mixer/patch[gain,hard,replace]/4x4 (Output)
                                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 52.0, lag: 0.01, out: 52.0
                                    1032 group (PostFaderSends)
                                        1102 mixer/patch[gain]/4x4 (Send)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 52.0, lag: 0.01, out: 48.0
                                    1098 mixer/levels/4 (PostfaderLevels)
                                        out: 52.0, gate: 1.0, lag: 0.01
                            1093 mixer/patch[hard,mix]/4x4 (RackOut)
                                active: 1.0, gate: 1.0, hard_gate: 1.0, in_: 48.0, lag: 0.01, mix: 1.0, out: 44.0
                    1089 mixer/levels/4 (PrefaderLevels)
                        out: 44.0, gate: 1.0, lag: 0.01
                    1034 group (PreFaderSends)
                    1090 mixer/patch[gain,hard,replace]/4x4 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 44.0, lag: 0.01, out: 44.0
                    1035 group (PostFaderSends)
                        1122 mixer/patch[gain]/4x4 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 44.0, lag: 0.01, out: 64.0
                    1091 mixer/levels/4 (PostfaderLevels)
                        out: 44.0, gate: 1.0, lag: 0.01
                1036 group (Two)
                    1037 group (Parameters)
                    1057 group (Receives)
                    1104 mixer/patch[fb,gain]/4x4 (Input)
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.01, out: 56.0
                    1043 group (SubTracks)
                        1044 group (Three)
                            1045 group (Parameters)
                            1052 group (Receives)
                            1109 mixer/patch[fb,gain]/4x4 (Input)
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.01, out: 60.0
                            1051 group (SubTracks)
                            1110 mixer/levels/4 (InputLevels)
                                out: 60.0, gate: 1.0, lag: 0.01
                            1053 group (Devices)
                            1111 mixer/levels/4 (PrefaderLevels)
                                out: 60.0, gate: 1.0, lag: 0.01
                            1054 group (PreFaderSends)
                            1112 mixer/patch[gain,hard,replace]/4x4 (Output)
                                active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 60.0, lag: 0.01, out: 60.0
                            1055 group (PostFaderSends)
                                1114 mixer/patch[gain]/4x4 (Send)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 60.0, lag: 0.01, out: 56.0
                            1113 mixer/levels/4 (PostfaderLevels)
                                out: 60.0, gate: 1.0, lag: 0.01
                    1105 mixer/levels/4 (InputLevels)
                        out: 56.0, gate: 1.0, lag: 0.01
                    1058 group (Devices)
                    1106 mixer/levels/4 (PrefaderLevels)
                        out: 56.0, gate: 1.0, lag: 0.01
                    1059 group (PreFaderSends)
                    1107 mixer/patch[gain,hard,replace]/4x4 (Output)
                        active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 56.0, lag: 0.01, out: 56.0
                    1060 group (PostFaderSends)
                        1123 mixer/patch[gain]/4x4 (Send)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 56.0, lag: 0.01, out: 64.0
                    1108 mixer/levels/4 (PostfaderLevels)
                        out: 56.0, gate: 1.0, lag: 0.01
            1061 group (MasterTrack)
                1062 group (Parameters)
                1068 group (Receives)
                1116 mixer/patch[fb,gain]/4x4 (Input)
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 36.0, lag: 0.01, out: 64.0
                1117 mixer/levels/4 (InputLevels)
                    out: 64.0, gate: 1.0, lag: 0.01
                1069 group (Devices)
                1118 mixer/levels/4 (PrefaderLevels)
                    out: 64.0, gate: 1.0, lag: 0.01
                1070 group (PreFaderSends)
                1119 mixer/patch[gain,hard,replace]/4x4 (Output)
                    active: 1.0, gain: 0.0, gate: 1.0, hard_gate: 1.0, in_: 64.0, lag: 0.01, out: 64.0
                1071 group (PostFaderSends)
                    1121 mixer/patch/4x2 (DirectOut)
                        active: 1.0, gate: 1.0, in_: 64.0, lag: 0.01, out: 0.0
                1120 mixer/levels/4 (PostfaderLevels)
                    out: 64.0, gate: 1.0, lag: 0.01
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