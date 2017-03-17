# -*- encoding: utf-8 -*-
import pathlib
from supriya import supriya_configuration
from supriya.tools import nonrealtimetools
from nonrealtimetools_testbase import TestCase


class TestCase(TestCase):

    def test_00a(self):
        """
        No input, no output file path specified, no render path specified.
        """
        session = self._make_session()
        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 10., 44100, 8, file_path=output_file_path)
        assert pathlib.Path(supriya_configuration.output_directory_path) in \
            output_file_path.parents
        assert self._sample(output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }

    def test_00b(self):
        """
        No input, no output file path specified, render path specified.
        """
        session = self._make_session()
        exit_code, output_file_path = session.render(
            render_directory_path=self.render_directory_path,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=output_file_path)
        assert pathlib.Path(self.render_directory_path) in \
            output_file_path.parents
        assert self._sample(output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }

    def test_00c(self):
        """
        No input, no output file path specified, no render path specified,
        output already exists.
        """
        session = self._make_session()
        osc_path = pathlib.Path().joinpath(
            supriya_configuration.output_directory_path,
            '7b3f85710f19667f73f745b8ac8080a0.osc',
            )
        aiff_path = pathlib.Path().joinpath(
            supriya_configuration.output_directory_path,
            '7b3f85710f19667f73f745b8ac8080a0.aiff',
            )
        if osc_path.exists():
            osc_path.unlink()
        if aiff_path.exists():
            aiff_path.unlink()

        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 10., 44100, 8, file_path=output_file_path)
        assert self._sample(output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        assert session.transcript == [
            'Writing 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Wrote 7b3f85710f19667f73f745b8ac8080a0.osc.',
            'Rendering 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Command: scsynth -N 7b3f85710f19667f73f745b8ac8080a0.osc _ 7b3f85710f19667f73f745b8ac8080a0.aiff 44100 aiff int24',
            '    Rendered 7b3f85710f19667f73f745b8ac8080a0.osc with exit code 0.',
            ]
        assert output_file_path == aiff_path
        assert osc_path.exists()
        assert aiff_path.exists()

        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 10., 44100, 8, file_path=output_file_path)
        assert self._sample(output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        assert session.transcript == [
            'Writing 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Skipped 7b3f85710f19667f73f745b8ac8080a0.osc. File already exists.',
            'Rendering 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Skipped 7b3f85710f19667f73f745b8ac8080a0.osc. Output already exists.',
            ]
        assert output_file_path == aiff_path
        assert osc_path.exists()
        assert aiff_path.exists()

        osc_path.unlink()

        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 10., 44100, 8, file_path=output_file_path)
        assert self._sample(output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        assert session.transcript == [
            'Writing 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Wrote 7b3f85710f19667f73f745b8ac8080a0.osc.',
            'Rendering 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Skipped 7b3f85710f19667f73f745b8ac8080a0.osc. Output already exists.',
            ]
        assert output_file_path == aiff_path
        assert osc_path.exists()
        assert aiff_path.exists()

        aiff_path.unlink()

        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 10., 44100, 8, file_path=output_file_path)
        assert self._sample(output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        assert session.transcript == [
            'Writing 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Skipped 7b3f85710f19667f73f745b8ac8080a0.osc. File already exists.',
            'Rendering 7b3f85710f19667f73f745b8ac8080a0.osc.',
            '    Command: scsynth -N 7b3f85710f19667f73f745b8ac8080a0.osc _ 7b3f85710f19667f73f745b8ac8080a0.aiff 44100 aiff int24',
            '    Rendered 7b3f85710f19667f73f745b8ac8080a0.osc with exit code 0.',
            ]
        assert output_file_path == aiff_path
        assert osc_path.exists()
        assert aiff_path.exists()

    def test_01(self):
        """
        No input.
        """
        session = self._make_session()
        synthdef = self._build_dc_synthdef(8)
        assert synthdef.anonymous_name == 'b47278d408f17357f6b260ec30ea213d'
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', synthdef.compile()],
                ['/s_new', 'b47278d408f17357f6b260ec30ea213d', 1000, 0, 0,
                    'source', 0]]],
            [2.0, [['/n_set', 1000, 'source', 0.25]]],
            [4.0, [['/n_set', 1000, 'source', 0.5]]],
            [6.0, [['/n_set', 1000, 'source', 0.75]]],
            [8.0, [['/n_set', 1000, 'source', 1.0]]],
            [10.0, [['/n_free', 1000], [0]]]]
        exit_code, _ = session.render(
            self.output_file_path,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8)
        assert self._sample(self.output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: 7b3f85710f19667f73f745b8ac8080a0
        source: null
        ''')

    def test_02(self):
        """
        Soundfile NRT input, matched channels.
        """
        path_one = self.output_directory_path / 'output-one.aiff'
        path_two = self.output_directory_path / 'output-two.aiff'
        session_one = self._make_session()
        exit_code, _ = session_one.render(
            path_one,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=path_one)
        session_two = nonrealtimetools.Session(input_=path_one)
        synthdef = self._build_multiplier_synthdef(8)
        with session_two.at(0):
            session_two.add_synth(
                synthdef=synthdef,
                duration=10,
                in_bus=session_two.audio_input_bus_group,
                out_bus=session_two.audio_output_bus_group,
                multiplier=-0.5,
                )
        exit_code, _ = session_two.render(
            path_two,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=path_two)
        assert self._sample(path_two) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [-0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125],
            0.41: [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
            0.61: [-0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375],
            0.81: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
            0.99: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
            }
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: 34a8138953258b32d05ed6e09ebdf5b7
        source: null
        ''')

    def test_03(self):
        """
        Soundfile NRT input, mismatched channels.
        """
        path_one = self.output_directory_path / 'output-one.aiff'
        path_two = self.output_directory_path / 'output-two.aiff'
        session_one = self._make_session()
        exit_code, _ = session_one.render(
            path_one,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=path_one)
        session_two = nonrealtimetools.Session(
            input_=path_one,
            input_bus_channel_count=2,
            output_bus_channel_count=4,
            )
        synthdef = self._build_multiplier_synthdef(4)
        with session_two.at(0):
            session_two.add_synth(
                synthdef=synthdef,
                duration=10,
                in_bus=session_two.audio_input_bus_group,
                out_bus=session_two.audio_output_bus_group,
                multiplier=-0.5,
                )
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '1d83a887914f0ac8ac3de461f4cc637c', 1000, 0, 0,
                    'in_bus', 4, 'multiplier', -0.5, 'out_bus', 0]]],
            [10.0, [['/n_free', 1000], [0]]]]
        exit_code, _ = session_two.render(
            path_two,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 4, file_path=path_two)
        assert self._sample(path_two) == {
            0.0: [0.0, 0.0, 0.0, 0.0],
            0.21: [-0.125, -0.125, -0.125, -0.125],
            0.41: [-0.25, -0.25, -0.25, -0.25],
            0.61: [-0.375, -0.375, -0.375, -0.375],
            0.81: [-0.5, -0.5, -0.5, -0.5],
            0.99: [-0.5, -0.5, -0.5, -0.5],
            }
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: f90a25f63698e1c8c4f6fe63d7d87bc4
        source: null
        ''')

    def test_04(self):
        """
        Session NRT input, matched channels.
        """
        session_one = self._make_session()
        session_two = nonrealtimetools.Session(
            input_=session_one,
            name='outer-session',
            )
        synthdef = self._build_multiplier_synthdef(8)
        with session_two.at(0):
            session_two.add_synth(
                synthdef=synthdef,
                duration=10,
                in_bus=session_two.audio_input_bus_group,
                out_bus=session_two.audio_output_bus_group,
                multiplier=-0.5,
                )
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '76abe8508565e1ca3dd243fe960a6945', 1000, 0, 0,
                    'in_bus', 8, 'multiplier', -0.5, 'out_bus', 0]]],
            [10.0, [['/n_free', 1000], [0]]]]
        exit_code, _ = session_two.render(
            self.output_file_path,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8)
        assert self._sample(self.output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [-0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125],
            0.41: [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
            0.61: [-0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375, -0.375],
            0.81: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
            0.99: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
            }
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: cf7a6b66194f0292ed98dd4190e02718
        source:
        - 7b3f85710f19667f73f745b8ac8080a0
        ''')

    def test_05(self):
        """
        Soundfile DiskIn input.
        """
        path_one = self.output_directory_path / 'output-one.aiff'
        path_two = self.output_directory_path / 'output-two.aiff'
        session_one = self._make_session()
        exit_code, _ = session_one.render(
            path_one,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=path_one)
        session_two = nonrealtimetools.Session()
        synthdef = self._build_diskin_synthdef(channel_count=8)
        with session_two.at(0):
            buffer_ = session_two.cue_soundfile(
                path_one,
                duration=10,
                )
            session_two.add_synth(
                synthdef=synthdef,
                buffer_id=buffer_,
                duration=10,
                )
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/b_alloc', 0, 32768, 8],
                ['/b_read', 0, str(path_one), 0, -1, 0, 1],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1000, 0, 0,
                    'buffer_id', 0]]],
            [10.0, [
                ['/n_free', 1000],
                ['/b_close', 0],
                ['/b_free', 0], [0]]]]
        exit_code, _ = session_two.render(
            path_two,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=path_two)
        assert self._sample(path_two) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: 7c7ca76f353e0a7bebdab29bc3f81f85
        source: null
        ''')

    def test_06(self):
        """
        Session DiskIn input.
        """
        session_one = self._make_session()
        session_two = nonrealtimetools.Session(name='outer-session')
        synthdef = self._build_diskin_synthdef(channel_count=8)
        with session_two.at(0):
            buffer_ = session_two.cue_soundfile(
                session_one,
                duration=10,
                )
            session_two.add_synth(
                synthdef=synthdef,
                buffer_id=buffer_,
                duration=10,
                )
        session_two.to_lists()
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/b_alloc', 0, 32768, 8],
                ['/b_read', 0, '7b3f85710f19667f73f745b8ac8080a0.aiff', 0, -1, 0, 1],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1000, 0, 0,
                    'buffer_id', 0]]],
            [10.0, [
                ['/n_free', 1000],
                ['/b_close', 0],
                ['/b_free', 0], [0]]]]
        exit_code, _ = session_two.render(
            self.output_file_path,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8)
        assert self._sample(self.output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: 99b3d6bd682960a74e8e78a0ad413600
        source:
        - 7b3f85710f19667f73f745b8ac8080a0
        ''')

    def test_07(self):
        """
        Chained Session DiskIn input.
        """
        session_one = self._make_session()
        session_two = nonrealtimetools.Session(name='middle-session')
        session_three = nonrealtimetools.Session(name='outer-session')
        diskin_synthdef = self._build_diskin_synthdef(channel_count=8)
        multiplier_synthdef = self._build_multiplier_synthdef(channel_count=8)
        with session_two.at(0):
            buffer_ = session_two.cue_soundfile(
                session_one,
                duration=10,
                )
            synth = session_two.add_synth(
                synthdef=diskin_synthdef,
                buffer_id=buffer_,
                duration=10,
                )
            synth.add_synth(
                add_action='ADD_AFTER',
                duration=10,
                synthdef=multiplier_synthdef,
                multiplier=-1.0,
                )
        with session_three.at(0):
            buffer_ = session_three.cue_soundfile(
                session_two,
                duration=10,
                )
            synth = session_three.add_synth(
                synthdef=diskin_synthdef,
                buffer_id=buffer_,
                duration=10,
                )
            synth.add_synth(
                add_action='ADD_AFTER',
                duration=10,
                synthdef=multiplier_synthdef,
                multiplier=-0.5,
                )

        d_recv_commands = []
        for synthdef in sorted(
            [diskin_synthdef, multiplier_synthdef],
            key=lambda x: x.anonymous_name,
            ):
            compiled_synthdef = bytearray(synthdef.compile())
            d_recv_commands.append(['/d_recv', compiled_synthdef])

        buffer_one_name = '7b3f85710f19667f73f745b8ac8080a0.aiff'
        assert session_two.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/b_alloc', 0, 32768, 8],
                ['/b_read', 0, buffer_one_name, 0, -1, 0, 1],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1000, 0, 0,
                    'buffer_id', 0],
                ['/s_new', '76abe8508565e1ca3dd243fe960a6945', 1001, 3, 1000,
                    'multiplier', -1.0]]],
            [10.0, [
                ['/n_free', 1000, 1001],
                ['/b_close', 0],
                ['/b_free', 0], [0]]]]

        buffer_two_name = 'd7a731a2149b910848fc46f08a586378.aiff'
        assert session_three.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/b_alloc', 0, 32768, 8],
                ['/b_read', 0, buffer_two_name, 0, -1, 0, 1],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1000, 0, 0,
                    'buffer_id', 0],
                ['/s_new', '76abe8508565e1ca3dd243fe960a6945', 1001, 3, 1000,
                    'multiplier', -0.5]]],
            [10.0, [
                ['/n_free', 1000, 1001],
                ['/b_close', 0],
                ['/b_free', 0], [0]]]]

        buffer_one_path = self.render_directory_path / buffer_one_name
        buffer_two_path = self.render_directory_path / buffer_two_name

        assert not buffer_one_path.exists()
        assert not buffer_two_path.exists()
        exit_code, _ = session_three.render(
            self.output_file_path,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=buffer_one_path)
        assert self._sample(buffer_one_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }
        self.assert_ok(exit_code, 10., 44100, 8, file_path=buffer_two_path)
        assert self._sample(buffer_two_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
            0.41: [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
            0.61: [-0.75, -0.75, -0.75, -0.75, -0.75, -0.75, -0.75, -0.75],
            0.81: [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            0.99: [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            }
        self.assert_ok(exit_code, 10., 44100, 8)
        assert self._sample(self.output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
            0.41: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.61: [0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375],
            0.81: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.99: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            }
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: f163f0fd844c070089704321bee40bcd
        source:
        - d7a731a2149b910848fc46f08a586378
        - 7b3f85710f19667f73f745b8ac8080a0
        ''')

    def test_08(self):
        """
        Fanned Session DiskIn input and NRT input.
        """
        session_one = self._make_session(multiplier=0.25)
        session_two = nonrealtimetools.Session(name='middle-session')
        session_three = nonrealtimetools.Session(name='outer-session')
        diskin_synthdef = self._build_diskin_synthdef(channel_count=8)
        with session_two.at(0):
            buffer_one = session_two.cue_soundfile(
                session_one,
                duration=10,
                )
            buffer_two = session_two.cue_soundfile(
                session_one,
                duration=10,
                )
            session_two.add_synth(
                synthdef=diskin_synthdef,
                buffer_id=buffer_one,
                duration=10,
                )
            session_two.add_synth(
                synthdef=diskin_synthdef,
                buffer_id=buffer_two,
                duration=10,
                )
        with session_three.at(0):
            buffer_one = session_three.cue_soundfile(
                session_one,
                duration=10,
                )
            buffer_two = session_three.cue_soundfile(
                session_two,
                duration=10,
                )
            session_three.add_synth(
                synthdef=diskin_synthdef,
                buffer_id=buffer_one,
                duration=10,
                )
            session_three.add_synth(
                synthdef=diskin_synthdef,
                buffer_id=buffer_two,
                duration=10,
                )
        assert session_one.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(self._build_dc_synthdef(8).compile())],
                ['/s_new', 'b47278d408f17357f6b260ec30ea213d', 1000, 0, 0,
                    'source', 0]]],
            [2.0, [['/n_set', 1000, 'source', 0.0625]]],
            [4.0, [['/n_set', 1000, 'source', 0.125]]],
            [6.0, [['/n_set', 1000, 'source', 0.1875]]],
            [8.0, [['/n_set', 1000, 'source', 0.25]]],
            [10.0, [['/n_free', 1000], [0]]]]
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(diskin_synthdef.compile())],
                ['/b_alloc', 0, 32768, 8],
                ['/b_alloc', 1, 32768, 8],
                ['/b_read', 0, 'c6d86f3d482a8bac1f7cc6650017da8e.aiff', 0, -1, 0, 1],
                ['/b_read', 1, 'c6d86f3d482a8bac1f7cc6650017da8e.aiff', 0, -1, 0, 1],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1000, 0, 0,
                    'buffer_id', 0],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1001, 0, 0,
                    'buffer_id', 1]]],
            [10.0, [
                ['/n_free', 1000, 1001],
                ['/b_close', 0],
                ['/b_free', 0],
                ['/b_close', 1],
                ['/b_free', 1],
                [0]]]]
        assert session_three.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(diskin_synthdef.compile())],
                ['/b_alloc', 0, 32768, 8],
                ['/b_alloc', 1, 32768, 8],
                ['/b_read', 0, 'c6d86f3d482a8bac1f7cc6650017da8e.aiff', 0, -1, 0, 1],
                ['/b_read', 1, '988ae28d3d84ae2b458d64ce15ffb989.aiff', 0, -1, 0, 1],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1000, 0, 0,
                    'buffer_id', 0],
                ['/s_new', '42367b5102dfa250b301ec698b3bd6c4', 1001, 0, 0,
                    'buffer_id', 1]]],
            [10.0, [
                ['/n_free', 1000, 1001],
                ['/b_close', 0],
                ['/b_free', 0],
                ['/b_close', 1],
                ['/b_free', 1],
                [0]]]]
        session_one_path = self.render_directory_path.joinpath(
            'c6d86f3d482a8bac1f7cc6650017da8e.aiff',
            )
        session_two_path = self.render_directory_path.joinpath(
            '988ae28d3d84ae2b458d64ce15ffb989.aiff',
            )
        exit_code, _ = session_three.render(
            self.output_file_path,
            render_directory_path=self.render_directory_path,
            build_render_yml=True,
            )
        self.assert_ok(exit_code, 10., 44100, 8, file_path=session_one_path)
        assert self._sample(session_one_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625],
            0.41: [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
            0.61: [0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875],
            0.81: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.99: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            }
        self.assert_ok(exit_code, 10., 44100, 8, file_path=session_two_path)
        assert self._sample(session_two_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
            0.41: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.61: [0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375],
            0.81: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.99: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            }
        self.assert_ok(exit_code, 10., 44100, 8)
        assert self._sample(self.output_file_path) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875],
            0.41: [0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375],
            0.61: [0.5625, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625],
            0.81: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.99: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            }
        assert session_three.transcript == [
            'Writing c6d86f3d482a8bac1f7cc6650017da8e.osc.',
            '    Wrote c6d86f3d482a8bac1f7cc6650017da8e.osc.',
            'Rendering c6d86f3d482a8bac1f7cc6650017da8e.osc.',
            '    Command: scsynth -N c6d86f3d482a8bac1f7cc6650017da8e.osc _ c6d86f3d482a8bac1f7cc6650017da8e.aiff 44100 aiff int24',
            '    Rendered c6d86f3d482a8bac1f7cc6650017da8e.osc with exit code 0.',
            'Writing 988ae28d3d84ae2b458d64ce15ffb989.osc.',
            '    Wrote 988ae28d3d84ae2b458d64ce15ffb989.osc.',
            'Rendering 988ae28d3d84ae2b458d64ce15ffb989.osc.',
            '    Command: scsynth -N 988ae28d3d84ae2b458d64ce15ffb989.osc _ 988ae28d3d84ae2b458d64ce15ffb989.aiff 44100 aiff int24',
            '    Rendered 988ae28d3d84ae2b458d64ce15ffb989.osc with exit code 0.',
            'Writing 73b90e1467ddd06f4afa06dff1f5cb41.osc.',
            '    Wrote 73b90e1467ddd06f4afa06dff1f5cb41.osc.',
            'Rendering 73b90e1467ddd06f4afa06dff1f5cb41.osc.',
            '    Command: scsynth -N 73b90e1467ddd06f4afa06dff1f5cb41.osc _ 73b90e1467ddd06f4afa06dff1f5cb41.aiff 44100 aiff int24',
            '    Rendered 73b90e1467ddd06f4afa06dff1f5cb41.osc with exit code 0.',
            'Writing output/render.yml.',
            '    Wrote output/render.yml.',
            ]
        assert self.render_yml_file_path.exists()
        self.compare_file_contents(self.render_yml_file_path, '''
        render: 73b90e1467ddd06f4afa06dff1f5cb41
        source:
        - 988ae28d3d84ae2b458d64ce15ffb989
        - c6d86f3d482a8bac1f7cc6650017da8e
        ''')
