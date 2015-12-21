# -*- encoding: utf-8 -*-
import os
import unittest
from supriya.tools import nrttools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(unittest.TestCase):

    def setUp(self):
        self.output_filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'output.aiff',
            ))
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def tearDown(self):
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def test_01(self):
        session = nrttools.Session()
        builder = synthdeftools.SynthDefBuilder()
        with builder:
            ugentools.Out.ar(bus=0, source=ugentools.SinOsc.ar())
        synthdef = builder.build()
        synth_one = nrttools.Synth(synthdef, 0, 1)
        session.insert([synth_one])
        exit_code, _ = session.render(self.output_filepath)
        assert os.path.exists(self.output_filepath)
        assert exit_code == 0
        soundfile = soundfiletools.SoundFile(self.output_filepath)
        assert float('{:.2f}'.format(soundfile.seconds)) == 1.
        assert soundfile.sample_rate == 44100
        assert soundfile.channel_count == 8
