import os
import pathlib
import pytest
import shutil
import supriya.nonrealtime
import supriya.realtime
import supriya.soundfiles
import supriya.synthdefs
import supriya.system
import supriya.ugens


class TestSessionFactory:

    def __init__(
        self,
        input_bus_channel_count=None,
        output_bus_channel_count=None,
        multiplier=1.0,
        ):
        options = supriya.realtime.ServerOptions(
            input_bus_channel_count=input_bus_channel_count,
            output_bus_channel_count=output_bus_channel_count,
            )
        self.input_bus_channel_count = options.input_bus_channel_count
        self.output_bus_channel_count = options.output_bus_channel_count
        self.multiplier = multiplier

    def _build_dc_synthdef(self, channel_count=1):
        with supriya.synthdefs.SynthDefBuilder(
            out_bus=0,
            source=0,
            ) as builder:
            source = supriya.ugens.K2A.ar(source=builder['source'])
            supriya.ugens.Out.ar(
                bus=builder['out_bus'],
                source=[source] * channel_count,
                )
        return builder.build()

    def __session__(self):
        session = supriya.nonrealtime.Session(
            input_bus_channel_count=self.input_bus_channel_count,
            output_bus_channel_count=self.output_bus_channel_count,
            name='inner-session',
            )
        output_bus_channel_count = session.options.output_bus_channel_count
        synthdef = self._build_dc_synthdef(
            channel_count=output_bus_channel_count,
            )
        with session.at(0):
            synth = session.add_synth(
                synthdef=synthdef,
                duration=10,
                source=0,
                )
        with session.at(2):
            synth['source'] = 0.25 * self.multiplier
        with session.at(4):
            synth['source'] = 0.5 * self.multiplier
        with session.at(6):
            synth['source'] = 0.75 * self.multiplier
        with session.at(8):
            synth['source'] = 1.0 * self.multiplier
        assert synthdef.anonymous_name == 'b47278d408f17357f6b260ec30ea213d'
        return session


class TestCase(supriya.system.TestCase):

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
            path.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        for path in [
            self.output_directory_path,
            self.render_directory_path,
            ]:
            if path.exists():
                shutil.rmtree(str(path))

    def build_basic_synthdef(self, bus=0):
        builder = supriya.synthdefs.SynthDefBuilder()
        with builder:
            supriya.ugens.Out.ar(
                bus=bus,
                source=supriya.ugens.SinOsc.ar(),
                )
        return builder.build()

    def build_duration_synthdef(self, bus=0):
        builder = supriya.synthdefs.SynthDefBuilder(duration=0)
        with builder:
            supriya.ugens.Out.ar(
                bus=bus,
                source=supriya.ugens.Line.ar(
                    duration=builder['duration'],
                    ),
                )
        return builder.build()

    def build_gate_synthdef(self, bus=0):
        builder = supriya.synthdefs.SynthDefBuilder(gate=1)
        with builder:
            envelope = supriya.synthdefs.Envelope.asr()
            envgen = supriya.ugens.EnvGen.ar(
                envelope=envelope,
                gate=builder['gate'],
                )
            source = supriya.ugens.Saw.ar() * envgen
            supriya.ugens.Out.ar(
                bus=bus,
                source=source,
                )
        return builder.build()

    def _make_session(
        self,
        input_=None,
        input_bus_channel_count=None,
        output_bus_channel_count=None,
        multiplier=1.0,
        ):
        session = supriya.nonrealtime.Session(
            input_bus_channel_count=input_bus_channel_count,
            output_bus_channel_count=output_bus_channel_count,
            name='inner-session',
            )
        output_bus_channel_count = session.options.output_bus_channel_count
        synthdef = self._build_dc_synthdef(
            channel_count=output_bus_channel_count,
            )
        with session.at(0):
            synth = session.add_synth(
                synthdef=synthdef,
                duration=10,
                source=0,
                )
        with session.at(2):
            synth['source'] = 0.25 * multiplier
        with session.at(4):
            synth['source'] = 0.5 * multiplier
        with session.at(6):
            synth['source'] = 0.75 * multiplier
        with session.at(8):
            synth['source'] = 1.0 * multiplier
        assert synthdef.anonymous_name == 'b47278d408f17357f6b260ec30ea213d'
        d_recv_commands = pytest.helpers.build_d_recv_commands([synthdef])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/s_new', 'b47278d408f17357f6b260ec30ea213d', 1000, 0, 0,
                    'source', 0]]],
            [2.0, [['/n_set', 1000, 'source', 0.25 * multiplier]]],
            [4.0, [['/n_set', 1000, 'source', 0.5 * multiplier]]],
            [6.0, [['/n_set', 1000, 'source', 0.75 * multiplier]]],
            [8.0, [['/n_set', 1000, 'source', 1.0 * multiplier]]],
            [10.0, [['/n_free', 1000], [0]]]
            ]
        return session

    def _make_session_factory(
        self,
        input_bus_channel_count=None,
        output_bus_channel_count=None,
        multiplier=1.0,
        ):
        session_factory = TestSessionFactory(
            input_bus_channel_count=input_bus_channel_count,
            output_bus_channel_count=output_bus_channel_count,
            multiplier=multiplier,
            )
        return session_factory

    def _build_dc_synthdef(self, channel_count=1):
        with supriya.synthdefs.SynthDefBuilder(
            out_bus=0,
            source=0,
            ) as builder:
            source = supriya.ugens.K2A.ar(source=builder['source'])
            supriya.ugens.Out.ar(
                bus=builder['out_bus'],
                source=[source] * channel_count,
                )
        return builder.build()

    def _build_diskin_synthdef(self, channel_count=1):
        with supriya.synthdefs.SynthDefBuilder(
            out_bus=0,
            buffer_id=0,
            ) as builder:
            source = supriya.ugens.DiskIn.ar(
                buffer_id=builder['buffer_id'],
                channel_count=channel_count,
                )
            supriya.ugens.Out.ar(
                bus=builder['out_bus'],
                source=source,
                )
        return builder.build()

    def _build_multiplier_synthdef(self, channel_count=1):
        with supriya.synthdefs.SynthDefBuilder(
            in_bus=0,
            out_bus=0,
            multiplier=1,
            ) as builder:
            source = supriya.ugens.In.ar(
                bus=builder['in_bus'],
                channel_count=channel_count,
                )
            supriya.ugens.ReplaceOut.ar(
                bus=builder['out_bus'],
                source=source * builder['multiplier'],
                )
        return builder.build()
