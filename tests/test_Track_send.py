import time
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
        self.server = supriya.realtime.Server().boot()
        self.mixer = livetools.Mixer(channel_count=1, cue_channel_count=1)
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
        self.mixer['foo'].set_gain(0)
        self.mixer['bar'].set_gain(0)
        self.mixer['baz'].set_gain(0)
        self.mixer['foo'].send['master'] = -96
        self.mixer['bar'].send['master'] = -96
        self.mixer['baz'].send['master'] = 0
        time.sleep(0.25)

    def tearDown(self):
        self.server.quit()

    def test_01(self):
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 0.25
        # chain bar into baz
        self.mixer['bar'].send['baz'] = 0
        time.sleep(0.25)
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 0.75
        # chain foo into bar
        self.mixer['foo'].send['bar'] = 0
        time.sleep(0.25)
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 1.75
        # mute bar
        self.mixer['bar'].set_mute(True)
        time.sleep(0.25)
        levels = self.mixer['master'].input_levels
        assert round(levels['rms'][0], 2) == 0.25
