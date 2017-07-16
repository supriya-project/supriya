import time
from abjad.tools import systemtools as abjad_systemtools
from supriya.tools import livetools
from supriya.tools import servertools
from supriya.tools import synthdeftools
from supriya.tools import systemtools
from supriya.tools import ugentools


class TestCase(abjad_systemtools.TestCase):

    with synthdeftools.SynthDefBuilder(out=0, value=1) as builder:
        source = ugentools.DC.ar(source=builder['value'])
        ugentools.Out.ar(bus=builder['out'], source=source)
    dc_synthdef = builder.build('dc')

    def setUp(self):
        super(abjad_systemtools.TestCase, self).setUp()
        self.server = servertools.Server().boot()
        self.mixer = livetools.Mixer(channel_count=1, cue_channel_count=1)
        self.mixer.add_track('track')

    def tearDown(self):
        self.server.quit()
        super(abjad_systemtools.TestCase, self).tearDown()

    def test_post_mixer_allocate(self):
        self.mixer.allocate()
        slot = self.mixer['track'].add_synth_slot(
            'synth',
            synthdef=self.dc_synthdef,
            value=0.5,
            )
        assert self.mixer['track']['synth'] is slot
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
                            1008 mixer/send/1x1
                                in_: 17.0, out: 0.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/1
                                in_: 18.0, out: 19.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/1
                                out: 19.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/send/1x1
                                in_: 19.0, out: 1.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
            """)

    def test_pre_mixer_allocate(self):
        slot = self.mixer['track'].add_synth_slot(
            'synth',
            synthdef=self.dc_synthdef,
            value=0.5,
            )
        assert self.mixer['track']['synth'] is slot
        self.mixer.allocate()
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
                            1008 mixer/send/1x1
                                in_: 17.0, out: 0.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/1
                                in_: 18.0, out: 19.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/1
                                out: 19.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/send/1x1
                                in_: 19.0, out: 1.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
            """)

    def test_play(self):
        slot = self.mixer['track'].add_synth_slot(
            'synth',
            synthdef=self.dc_synthdef,
            value=0.5,
            )
        self.mixer.allocate()
        slot.play(True)
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
                                        1023 dc
                                            out: 21.0, value: 0.5
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
                            1008 mixer/send/1x1
                                in_: 17.0, out: 0.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/1
                                in_: 18.0, out: 19.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/1
                                out: 19.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/send/1x1
                                in_: 19.0, out: 1.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1

            """)

    def test_stop(self):
        slot = self.mixer['track'].add_synth_slot(
            'synth',
            synthdef=self.dc_synthdef,
            value=0.5,
            )
        self.mixer.allocate()
        assert slot.play(True)
        time.sleep(0.25)
        assert not slot.play(False)
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
                            1008 mixer/send/1x1
                                in_: 17.0, out: 0.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/1
                                in_: 18.0, out: 19.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/1
                                out: 19.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/send/1x1
                                in_: 19.0, out: 1.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
            """)

    def test___getitem__(self):
        """
        Subscripting returns bindable namespace proxies.
        """
        slot = self.mixer['track'].add_synth_slot(
            'synth',
            synthdef=self.dc_synthdef,
            value=0.5,
            )
        assert isinstance(slot['value'], systemtools.BindableFloat)
        assert slot['value'].value == 0.5

    def test___setitem__01(self):
        """
        Can set synth controls when synth is allocated.
        """
        self.mixer.allocate()
        slot = self.mixer['track'].add_synth_slot(
            'synth',
            synthdef=self.dc_synthdef,
            value=0.5,
            )
        assert sorted(slot.bindable_namespace.items()) == [('value', 0.5)]
        assert slot.synth['value'].value == 0.5
        slot.play(True)
        assert sorted(slot.bindable_namespace.items()) == [('value', 0.5)]
        assert slot.synth['value'].value == 0.5
        slot['value'] = 0.25
        assert sorted(slot.bindable_namespace.items()) == [('value', 0.25)]
        assert slot.synth['value'].value == 0.25
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
                            1008 mixer/send/1x1
                                in_: 17.0, out: 0.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/1
                                in_: 18.0, out: 19.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/1
                                out: 19.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/send/1x1
                                in_: 19.0, out: 1.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
            """)

    def test___setitem__02(self):
        """
        Can set synth controls when synth is not allocated.
        """
        self.mixer.allocate()
        slot = self.mixer['track'].add_synth_slot(
            'synth',
            synthdef=self.dc_synthdef,
            value=0.5,
            )
        assert sorted(slot.bindable_namespace.items()) == [('value', 0.5)]
        assert slot.synth['value'].value == 0.5
        slot['value'] = 0.25
        assert sorted(slot.bindable_namespace.items()) == [('value', 0.25)]
        assert slot.synth['value'].value == 0.25
        slot.play(True)
        assert sorted(slot.bindable_namespace.items()) == [('value', 0.25)]
        assert slot.synth['value'].value == 0.25
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
                            1008 mixer/send/1x1
                                in_: 17.0, out: 0.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                        1009 group
                            1010 mixer/input/1
                                in_: 18.0, out: 19.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
                            1011 group
                            1012 mixer/output/1
                                out: 19.0, active: 1.0, gain: -96.0, gate: 1.0, lag: 0.1
                            1013 group
                            1014 mixer/send/1x1
                                in_: 19.0, out: 1.0, active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1
            """)
