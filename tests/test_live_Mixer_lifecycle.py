from supriya.tools import livetools
import supriya.realtime
from supriya.tools import synthdeftools
from supriya.tools import systemtools
from supriya.tools import ugentools


class TestCase(systemtools.TestCase):

    with synthdeftools.SynthDefBuilder(out=0, value=1) as builder:
        source = ugentools.DC.ar(source=builder['value'])
        ugentools.Out.ar(bus=builder['out'], source=source)

    dc_synthdef = builder.build('dc')

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_01(self):
        mixer = livetools.Mixer(channel_count=4)
        self.compare_strings(
            str(self.server),
            """
            NODE TREE 0 group
                1 group
            """)
        mixer.allocate()
        mixer.add_track('foo')
        mixer.add_track('bar')
        self.compare_strings(
            str(self.server),
            """
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 group
                            1015 group
                                1016 mixer/input/4
                                    in_: 28.0, out: 32.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1017 group
                                1018 mixer/send/4x2
                                    in_: 32.0, out: 24.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1019 mixer/output/4
                                    out: 32.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1020 group
                                    1021 mixer/send/4x4
                                        in_: 32.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1022 group
                                1023 mixer/input/4
                                    in_: 36.0, out: 40.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1024 group
                                1025 mixer/send/4x2
                                    in_: 40.0, out: 24.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1026 mixer/output/4
                                    out: 40.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1027 group
                                    1028 mixer/send/4x4
                                        in_: 40.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1002 group
                            1003 mixer/input/4
                                in_: 16.0, out: 20.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1004 group
                            1005 mixer/send/4x2
                                in_: 20.0, out: 24.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1006 mixer/output/4
                                out: 20.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1007 group
                            1008 mixer/direct/0:0,1:1,2:2,3:3
                                in_: 20.0, out: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/2
                                in_: 24.0, out: 26.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/2
                                out: 26.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/direct/0:4,1:5
                                in_: 26.0, out: 0.0, gate: 1.0, lag: 0.1
            """)
        for track_name in ('master', 'cue', 'foo', 'bar'):
            track = mixer[track_name]
            assert track.name == track_name
            assert track.input_bus_group.is_allocated
            assert track.output_bus_group.is_allocated
        mixer.free()
        self.compare_strings(
            str(self.server),
            """
            NODE TREE 0 group
                1 group
            """)
        for track_name in ('master', 'cue', 'foo', 'bar'):
            track = mixer[track_name]
            assert track.name == track_name
            assert not track.input_bus_group.is_allocated
            assert not track.output_bus_group.is_allocated

    def test_02(self):
        mixer = livetools.Mixer(channel_count=4)
        self.compare_strings(
            str(self.server),
            """
            NODE TREE 0 group
                1 group
            """)
        mixer.add_track('foo')
        mixer.add_track('bar')
        mixer.allocate()
        self.compare_strings(
            str(self.server),
            """
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 group
                            1015 group
                                1016 mixer/input/4
                                    in_: 28.0, out: 32.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1017 group
                                1018 mixer/send/4x2
                                    in_: 32.0, out: 24.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1019 mixer/output/4
                                    out: 32.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1020 group
                                    1021 mixer/send/4x4
                                        in_: 32.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1022 group
                                1023 mixer/input/4
                                    in_: 36.0, out: 40.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1024 group
                                1025 mixer/send/4x2
                                    in_: 40.0, out: 24.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1026 mixer/output/4
                                    out: 40.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1027 group
                                    1028 mixer/send/4x4
                                        in_: 40.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1002 group
                            1003 mixer/input/4
                                in_: 16.0, out: 20.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1004 group
                            1005 mixer/send/4x2
                                in_: 20.0, out: 24.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1006 mixer/output/4
                                out: 20.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1007 group
                            1008 mixer/direct/0:0,1:1,2:2,3:3
                                in_: 20.0, out: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/2
                                in_: 24.0, out: 26.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/2
                                out: 26.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/direct/0:4,1:5
                                in_: 26.0, out: 0.0, gate: 1.0, lag: 0.1
            """)
        for track_name in ('master', 'cue', 'foo', 'bar'):
            track = mixer[track_name]
            assert track.name == track_name
            assert track.input_bus_group.is_allocated
            assert track.output_bus_group.is_allocated
        mixer.free()
        self.compare_strings(
            str(self.server),
            """
            NODE TREE 0 group
                1 group
            """)
        for track_name in ('master', 'cue', 'foo', 'bar'):
            track = mixer[track_name]
            assert track.name == track_name
            assert not track.input_bus_group.is_allocated
            assert not track.output_bus_group.is_allocated

    def test_03(self):
        """
        Common setup for other tests.
        """
        mixer = livetools.Mixer(channel_count=1, cue_channel_count=1)
        mixer.add_track('foo')
        mixer.add_track('bar')
        mixer.add_track('baz')
        mixer.allocate()
        synth_a = supriya.realtime.Synth(synthdef=self.dc_synthdef, value=1.0)
        synth_b = supriya.realtime.Synth(synthdef=self.dc_synthdef, value=0.5)
        synth_c = supriya.realtime.Synth(synthdef=self.dc_synthdef, value=0.25)
        synth_a.allocate(
            target_node=mixer['foo'],
            out=int(mixer['foo'].output_bus_group),
            )
        synth_b.allocate(
            target_node=mixer['bar'],
            out=int(mixer['bar'].output_bus_group),
            )
        synth_c.allocate(
            target_node=mixer['baz'],
            out=int(mixer['baz'].output_bus_group),
            )
        self.compare_strings(
            str(self.server),
            """
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 group
                            1015 group
                                1016 mixer/input/1
                                    in_: 20.0, out: 21.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1017 group
                                    1036 dc
                                        out: 21.0, value: 1.0
                                1018 mixer/send/1x1
                                    in_: 21.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1019 mixer/output/1
                                    out: 21.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1020 group
                                    1021 mixer/send/1x1
                                        in_: 21.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1022 group
                                1023 mixer/input/1
                                    in_: 22.0, out: 23.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1024 group
                                    1037 dc
                                        out: 23.0, value: 0.5
                                1025 mixer/send/1x1
                                    in_: 23.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1026 mixer/output/1
                                    out: 23.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1027 group
                                    1028 mixer/send/1x1
                                        in_: 23.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1029 group
                                1030 mixer/input/1
                                    in_: 24.0, out: 25.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1031 group
                                    1038 dc
                                        out: 25.0, value: 0.25
                                1032 mixer/send/1x1
                                    in_: 25.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1033 mixer/output/1
                                    out: 25.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1034 group
                                    1035 mixer/send/1x1
                                        in_: 25.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1002 group
                            1003 mixer/input/1
                                in_: 16.0, out: 17.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1004 group
                            1005 mixer/send/1x1
                                in_: 17.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1006 mixer/output/1
                                out: 17.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1007 group
                            1008 mixer/direct/0:0
                                in_: 17.0, out: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/1
                                in_: 18.0, out: 19.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/1
                                out: 19.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/direct/0:1
                                in_: 19.0, out: 0.0, gate: 1.0, lag: 0.1
            """)
