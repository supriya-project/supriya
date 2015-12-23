# -*- encoding: utf-8 -*-
import os
import unittest
from abjad.tools import timespantools
from supriya.tools import nrttools
from supriya.tools import osctools
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
        synth_one = nrttools.Synth(0, 1, synthdef=self.build_synthdef())
        session.insert([synth_one])
        exit_code, _ = session.render(self.output_filepath)
        self.assert_ok(exit_code, 1., 44100, 8)

    def test_02(self):
        session = nrttools.Session()
        synth_one = nrttools.Synth(0, 300, synthdef=self.build_synthdef())
        session.insert([synth_one])
        exit_code, _ = session.render(
            self.output_filepath,
            sample_rate=48000,
            output_bus_channel_count=2,
            )
        self.assert_ok(exit_code, 300., 48000, 2)

    def test_03(self):
        session = nrttools.Session()
        synth_one = nrttools.Synth(1, 2, synthdef=self.build_synthdef())
        session.insert([synth_one])
        timespan = timespantools.Timespan(0.5, 2.5)
        assert session.to_osc_bundles(timespan=timespan) == [
            osctools.OscBundle(
                timestamp=0.5,
                contents=(
                    osctools.OscMessage(5, bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 d719856d7deff2696a3f807f5dc79809\x00\x00\x00\x02C\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage(9, 'd719856d7deff2696a3f807f5dc79809', 1000, 1, 0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.5,
                contents=(
                    osctools.OscMessage(11, 1000),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.5,
                contents=(
                    osctools.OscMessage(0),
                    )
                ),
            ]
