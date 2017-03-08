# -*- encoding: utf-8 -*-
import os
import pathlib
import shutil
from abjad.tools import systemtools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(systemtools.TestCase):

    test_path = pathlib.Path(__file__).parent

    def setUp(self):
        self.directory_items = set(self.test_path.iterdir())
        self.output_directory = os.path.dirname(__file__)
        self.output_file_path = os.path.abspath(os.path.join(
            self.output_directory, 'output.aiff',
            ))
        self.render_yml_path = os.path.abspath(os.path.join(
            self.output_directory, 'render.yml',
            ))
        self.original_curdir = os.path.abspath(os.curdir)
        os.chdir(self.output_directory)

    def tearDown(self):
        for path in sorted(self.test_path.iterdir()):
            if path in self.directory_items:
                continue
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(str(path))
        os.chdir(self.original_curdir)

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
        exit_code,
        expected_duration,
        expected_sample_rate,
        expected_channel_count,
        file_path=None,
        ):
        file_path = str(file_path or self.output_file_path)
        assert os.path.exists(file_path), file_path
        assert exit_code == 0, exit_code
        soundfile = soundfiletools.SoundFile(file_path)
        assert self.round(soundfile.seconds) == expected_duration, self.round(soundfile.seconds)
        assert soundfile.sample_rate == expected_sample_rate, soundfile.sample_rate
        assert soundfile.channel_count == expected_channel_count, soundfile.channel_count
