# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(systemtools.TestCase):

    def setUp(self):
        self.output_filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__),  # relative to the base class
            'output.aiff',
            ))
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def tearDown(self):
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def build_basic_synthdef(self, bus=0):
        builder = synthdeftools.SynthDefBuilder()
        with builder:
            ugentools.Out.ar(
                bus=bus,
                source=ugentools.SinOsc.ar(),
                )
        return builder.build()

    def build_duration_synthdef(self, bus=0):
        builder = synthdeftools.SynthDefBuilder(duration=0)
        with builder:
            ugentools.Out.ar(
                bus=bus,
                source=ugentools.Line.ar(
                    duration=builder['duration'],
                    ),
                )
        return builder.build()

    def build_gate_synthdef(self, bus=0):
        builder = synthdeftools.SynthDefBuilder(gate=1)
        with builder:
            envelope = synthdeftools.Envelope.asr()
            envgen = ugentools.EnvGen.ar(
                envelope=envelope,
                gate=builder['gate'],
                )
            source = ugentools.Saw.ar() * envgen
            ugentools.Out.ar(
                bus=bus,
                source=source,
                )
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
