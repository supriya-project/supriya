import time
import supriya.live
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
        self.server = supriya.realtime.Server().boot()
        self.mixer = supriya.live.Mixer(channel_count=1, cue_channel_count=1)
        self.mixer.add_track('foo')
        self.mixer.add_track('bar')
        self.mixer.add_track('baz')
        self.mixer.allocate()
        synth_a = supriya.realtime.Synth(synthdef=self.dc_synthdef, value=1.0)
        synth_b = supriya.realtime.Synth(synthdef=self.dc_synthdef, value=0.5)
        synth_c = supriya.realtime.Synth(synthdef=self.dc_synthdef, value=0.25)
        synth_a.allocate(
            target_node=self.mixer['foo'],
            out=int(self.mixer['foo'].output_bus_group),
            )
        synth_b.allocate(
            target_node=self.mixer['bar'],
            out=int(self.mixer['bar'].output_bus_group),
            )
        synth_c.allocate(
            target_node=self.mixer['baz'],
            out=int(self.mixer['baz'].output_bus_group),
            )
        time.sleep(0.25)

    def tearDown(self):
        self.server.quit()

    def test_01(self):
        """
        Tracks are initially uncued.
        """
        assert not self.mixer['foo'].is_cued
        assert not self.mixer['bar'].is_cued
        assert not self.mixer['baz'].is_cued
        assert not self.mixer['foo'].cue_synth['active'].value
        assert not self.mixer['bar'].cue_synth['active'].value
        assert not self.mixer['baz'].cue_synth['active'].value
        time.sleep(0.1)
        levels = self.mixer['cue'].input_levels
        assert round(levels['rms'][0], 2) == 0.0

    def test_02(self):
        """
        Tracks can be cued.
        """
        self.mixer['bar'].set_cue(True)
        time.sleep(0.2)
        assert not self.mixer['foo'].is_cued
        assert self.mixer['bar'].is_cued
        assert not self.mixer['baz'].is_cued
        assert not self.mixer['foo'].cue_synth['active'].value
        assert self.mixer['bar'].cue_synth['active'].value
        assert not self.mixer['baz'].cue_synth['active'].value
        levels = self.mixer['cue'].input_levels
        assert round(levels['rms'][0], 2) == 0.5

    def test_03(self):
        """
        Cued tracks can be uncued.
        """
        self.mixer['bar'].set_cue(True)
        self.mixer['bar'].set_cue(False)
        time.sleep(0.2)
        assert not self.mixer['foo'].is_cued
        assert not self.mixer['bar'].is_cued
        assert not self.mixer['baz'].is_cued
        assert not self.mixer['foo'].cue_synth['active'].value
        assert not self.mixer['bar'].cue_synth['active'].value
        assert not self.mixer['baz'].cue_synth['active'].value
        levels = self.mixer['cue'].input_levels
        assert round(levels['rms'][0], 2) == 0.0

    def test_04(self):
        """
        Mutually-exclusive, by default.
        """
        self.mixer['bar'].set_cue(True)
        self.mixer['baz'].set_cue(True)
        time.sleep(0.2)
        assert not self.mixer['foo'].is_cued
        assert not self.mixer['bar'].is_cued
        assert self.mixer['baz'].is_cued
        assert not self.mixer['foo'].cue_synth['active'].value
        assert not self.mixer['bar'].cue_synth['active'].value
        assert self.mixer['baz'].cue_synth['active'].value
        levels = self.mixer['cue'].input_levels
        assert round(levels['rms'][0], 2) == 0.25

    def test_05(self):
        """
        Not mutually-exclusive, when Mixer.is_allowing_multiple.
        """
        self.mixer['bar'].set_cue(True)
        self.mixer.allow_multiple(True)
        self.mixer['baz'].set_cue(True)
        time.sleep(0.2)
        assert not self.mixer['foo'].is_cued
        assert self.mixer['bar'].is_cued
        assert self.mixer['baz'].is_cued
        assert not self.mixer['foo'].cue_synth['active'].value
        assert self.mixer['bar'].cue_synth['active'].value
        assert self.mixer['baz'].cue_synth['active'].value
        levels = self.mixer['cue'].input_levels
        assert round(levels['rms'][0], 2) == 0.75

    def test_06(self):
        """
        Mutually-exclusive again, when not Mixer.is_allowing_multiple.
        """
        self.mixer['bar'].set_cue(True)
        self.mixer.allow_multiple(True)
        self.mixer['baz'].set_cue(True)
        self.mixer.allow_multiple(False)
        self.mixer['foo'].set_cue(True)
        time.sleep(0.2)
        assert self.mixer['foo'].is_cued
        assert not self.mixer['bar'].is_cued
        assert not self.mixer['baz'].is_cued
        assert self.mixer['foo'].cue_synth['active'].value
        assert not self.mixer['bar'].cue_synth['active'].value
        assert not self.mixer['baz'].cue_synth['active'].value
        levels = self.mixer['cue'].input_levels
        assert round(levels['rms'][0], 2) == 1.0
