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

    def build_synthdef(self, bus=0):
        builder = synthdeftools.SynthDefBuilder()
        with builder:
            ugentools.Out.ar(bus=0, source=ugentools.SinOsc.ar())
        return builder.build()

    def round(self, value):
        return float('{:.2f}'.format(value))

    def assert_ok(
        self,
        expected_exit_code,
        expected_duration,
        expected_sample_rate,
        expected_channel_count,
        ):
        assert os.path.exists(self.output_filepath)
        assert expected_exit_code == 0
        soundfile = soundfiletools.SoundFile(self.output_filepath)
        assert self.round(soundfile.seconds) == expected_duration
        assert soundfile.sample_rate == expected_sample_rate
        assert soundfile.channel_count == expected_channel_count

    def test_01(self):
        session = nrttools.Session()
        synth_one = nrttools.Synth(self.build_synthdef(), 0, 1)
        session.insert([synth_one])
        exit_code, _ = session.render(self.output_filepath)
        self.assert_ok(exit_code, 1., 44100, 8)

    def test_02(self):
        session = nrttools.Session()
        synth_one = nrttools.Synth(self.build_synthdef(), 0, 300)
        session.insert([synth_one])
        exit_code, _ = session.render(
            self.output_filepath,
            sample_rate=48000,
            output_bus_channel_count=2,
            )
        self.assert_ok(exit_code, 300., 48000, 2)
