# -*- encoding: utf-8 -*-
import os
import pathlib
import shutil
from abjad.tools import systemtools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(systemtools.TestCase):

    test_directory_path = pathlib.Path(__file__).parent
    output_directory_path = test_directory_path / 'output'
    render_directory_path = test_directory_path / 'render'
    output_file_path = output_directory_path / 'output.aiff'
    render_yml_file_path = output_directory_path / 'render.yml'

    @classmethod
    def setUpClass(cls):
        cls.original_curdir = os.path.abspath(os.curdir)
        os.chdir(str(cls.test_directory_path))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.original_curdir)

    def setUp(self):
        for path in [
            self.output_directory_path,
            self.render_directory_path,
            ]:
            if not path.exists():
                path.mkdir()

    def tearDown(self):
        for path in [
            self.output_directory_path,
            self.render_directory_path,
            ]:
            if path.exists():
                shutil.rmtree(str(path))

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
        file_path = pathlib.Path(file_path or self.output_file_path)
        assert file_path.exists(), file_path
        assert exit_code == 0, exit_code
        soundfile = soundfiletools.SoundFile(file_path)
        assert self.round(soundfile.seconds) == expected_duration, self.round(soundfile.seconds)
        assert soundfile.sample_rate == expected_sample_rate, soundfile.sample_rate
        assert soundfile.channel_count == expected_channel_count, soundfile.channel_count
