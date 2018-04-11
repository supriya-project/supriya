import supriya.live
import supriya.patterns
import supriya.realtime
import supriya.synthdefs
from supriya.tools import systemtools
import supriya.ugens


class TestCase(systemtools.TestCase):

    with supriya.synthdefs.SynthDefBuilder(out=0, value=1) as builder:
        source = supriya.ugens.DC.ar(source=builder['value'])
        supriya.ugens.Out.ar(bus=builder['out'], source=source)
    dc_synthdef = builder.build('dc')

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()
        self.mixer = supriya.live.Mixer(channel_count=1, cue_channel_count=1)
        self.mixer.add_track('track')

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_post_mixer_allocate(self):
        self.mixer.allocate()
        pattern = supriya.patterns.Pbind(
            value=supriya.patterns.Pseq([0.25, 0.5, 1.0, 2.0], None),
            )
        slot = self.mixer['track'].add_trigger_pattern_slot(
            'trigger',
            synthdef=self.dc_synthdef,
            pattern=pattern,
            )
        assert self.mixer['track']['trigger'] is slot
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
                                    1022 group
                                1018 mixer/send/1x1
                                    in_: 21.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1019 mixer/output/1
                                    out: 21.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1020 group
                                    1021 mixer/send/1x1
                                        in_: 21.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
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

    def test_trigger(self):
        self.mixer.allocate()
        pattern = supriya.patterns.Pbind(
            value=supriya.patterns.Pseq([0.25, 0.5, 1.0, 2.0], None),
            )
        slot = self.mixer['track'].add_trigger_pattern_slot(
            'trigger',
            synthdef=self.dc_synthdef,
            pattern=pattern,
            )
        slot.trigger(True)
        slot.trigger(True)
        slot.trigger(True)
        slot.trigger(True)
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
                                    1022 group
                                        1026 dc
                                            out: 21.0, value: 2.0
                                        1025 dc
                                            out: 21.0, value: 1.0
                                        1024 dc
                                            out: 21.0, value: 0.5
                                        1023 dc
                                            out: 21.0, value: 0.25
                                1018 mixer/send/1x1
                                    in_: 21.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1019 mixer/output/1
                                    out: 21.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1020 group
                                    1021 mixer/send/1x1
                                        in_: 21.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
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

    def test_maximum_replicas(self):
        self.mixer.allocate()
        pattern = supriya.patterns.Pbind(
            value=supriya.patterns.Pseq([1, 2, 3, 4, 5], None),
            )
        slot = self.mixer['track'].add_trigger_pattern_slot(
            'trigger',
            synthdef=self.dc_synthdef,
            pattern=pattern,
            maximum_replicas=4,
            )
        slot.trigger(True)
        slot.trigger(True)
        slot.trigger(True)
        slot.trigger(True)
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
                                    1022 group
                                        1026 dc
                                            out: 21.0, value: 4.0
                                        1025 dc
                                            out: 21.0, value: 3.0
                                        1024 dc
                                            out: 21.0, value: 2.0
                                        1023 dc
                                            out: 21.0, value: 1.0
                                1018 mixer/send/1x1
                                    in_: 21.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1019 mixer/output/1
                                    out: 21.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1020 group
                                    1021 mixer/send/1x1
                                        in_: 21.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
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
        slot.trigger(True)
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
                                    1022 group
                                        1027 dc
                                            out: 21.0, value: 5.0
                                        1026 dc
                                            out: 21.0, value: 4.0
                                        1025 dc
                                            out: 21.0, value: 3.0
                                        1024 dc
                                            out: 21.0, value: 2.0
                                1018 mixer/send/1x1
                                    in_: 21.0, out: 18.0, active: 0.0, gain: 0.0, gate: 1.0, lag: 0.1
                                1019 mixer/output/1
                                    out: 21.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                                1020 group
                                    1021 mixer/send/1x1
                                        in_: 21.0, out: 16.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
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