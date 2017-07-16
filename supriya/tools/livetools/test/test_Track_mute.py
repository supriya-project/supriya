import time
from abjad.tools import systemtools
from supriya.tools import livetools
from supriya.tools import servertools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(systemtools.TestCase):

    with synthdeftools.SynthDefBuilder(out=0, value=1) as builder:
        source = ugentools.DC.ar(source=builder['value'])
        ugentools.Out.ar(bus=builder['out'], source=source)

    dc_synthdef = builder.build('dc')

    def setUp(self):
        self.server = servertools.Server().boot()
        self.mixer = livetools.Mixer(channel_count=1, cue_channel_count=1)
        self.mixer.add_track('foo')
        self.mixer.add_track('bar')
        self.mixer.add_track('baz')
        self.mixer.allocate()
        synth_a = servertools.Synth(synthdef=self.dc_synthdef, value=1.0)
        synth_b = servertools.Synth(synthdef=self.dc_synthdef, value=0.5)
        synth_c = servertools.Synth(synthdef=self.dc_synthdef, value=0.25)
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
        self.mixer['foo'].gain(0)
        self.mixer['bar'].gain(0)
        self.mixer['baz'].gain(0)
        time.sleep(0.25)

    def tearDown(self):
        self.server.quit()

    def test_01(self):
        """
        Tracks are initially unmuted.
        """
        assert not self.mixer['foo'].is_muted
        assert not self.mixer['bar'].is_muted
        assert not self.mixer['baz'].is_muted
        assert self.mixer['foo'].output_synth['active'].value
        assert self.mixer['bar'].output_synth['active'].value
        assert self.mixer['baz'].output_synth['active'].value
        time.sleep(0.5)
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 1.75

    def test_02(self):
        """
        Tracks can be muted.
        """
        self.mixer['bar'].mute(True)
        time.sleep(0.25)
        assert not self.mixer['foo'].is_muted
        assert self.mixer['bar'].is_muted
        assert not self.mixer['baz'].is_muted
        assert self.mixer['foo'].output_synth['active'].value
        assert not self.mixer['bar'].output_synth['active'].value
        assert self.mixer['baz'].output_synth['active'].value
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 1.25

    def test_03(self):
        """
        Tracks can be unmuted.
        """
        self.mixer['bar'].mute(True)
        self.mixer['bar'].mute(False)
        time.sleep(0.25)
        assert not self.mixer['foo'].is_muted
        assert not self.mixer['bar'].is_muted
        assert not self.mixer['baz'].is_muted
        assert self.mixer['foo'].output_synth['active'].value
        assert self.mixer['bar'].output_synth['active'].value
        assert self.mixer['baz'].output_synth['active'].value
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 1.75

    def test_04(self):
        """
        Muting is not mutally exclusive.
        """
        self.mixer['bar'].mute(True)
        self.mixer['foo'].mute(True)
        time.sleep(0.25)
        assert self.mixer['foo'].is_muted
        assert self.mixer['bar'].is_muted
        assert not self.mixer['baz'].is_muted
        assert not self.mixer['foo'].output_synth['active'].value
        assert not self.mixer['bar'].output_synth['active'].value
        assert self.mixer['baz'].output_synth['active'].value
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 0.25
