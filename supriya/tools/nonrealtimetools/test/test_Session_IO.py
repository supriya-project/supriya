# -*- encoding: utf-8 -*-
import os
import unittest
from supriya.tools import nonrealtimetools
from supriya.tools import soundfiletools
from supriya.tools import synthdeftools
from supriya.tools import ugentools
from nonrealtimetools_testbase import TestCase


class TestCase(TestCase):

    # TODO: Session bus references should use Audio(Input|Output)BusGroup.
    #       That will help make sessions portable across different renders.

    def build_dc_synthdef(self, channel_count=1):
        with synthdeftools.SynthDefBuilder(
            out_bus=0,
            source=0,
            ) as builder:
            source = ugentools.K2A.ar(source=builder['source'])
            ugentools.Out.ar(
                bus=builder['out_bus'],
                source=[source] * channel_count,
                )
        return builder.build()

    def build_diskin_synthdef(self, channel_count=1):
        with synthdeftools.SynthDefBuilder(
            out_bus=0,
            buffer_id=0,
            ) as builder:
            source = ugentools.DiskIn.ar(
                buffer_id=builder['buffer_id'],
                channel_count=channel_count,
                )
            ugentools.Out.ar(
                bus=builder['out_bus'],
                source=source,
                )
        return builder.build()

    def build_multiplier_synthdef(self, channel_count=1):
        with synthdeftools.SynthDefBuilder(
            in_bus=0,
            out_bus=0,
            multiplier=1,
            ) as builder:
            source = ugentools.In.ar(
                bus=builder['in_bus'],
                channel_count=channel_count,
                )
            ugentools.Out.ar(
                bus=builder['out_bus'],
                source=source * builder['multiplier'],
                )
        return builder.build()

    def _make_session(self, input_bus_channel_count=None, output_bus_channel_count=None):
        session = nonrealtimetools.Session(
            input_bus_channel_count=input_bus_channel_count,
            output_bus_channel_count=output_bus_channel_count,
            )
        output_bus_channel_count = session.options.output_bus_channel_count
        synthdef = self.build_dc_synthdef(channel_count=output_bus_channel_count)
        with session.at(0):
            synth = session.add_synth(
                synthdef=synthdef,
                duration=10,
                source=0,
                )
        with session.at(2):
            synth['source'] = 0.25
        with session.at(4):
            synth['source'] = 0.5
        with session.at(6):
            synth['source'] = 0.75
        with session.at(8):
            synth['source'] = 1.0
        return session

    def _sample(self, filepath):
        soundfile = soundfiletools.SoundFile(filepath)
        return {
            0.0: [round(x, 6) for x in soundfile.at_percent(0)],
            0.21: [round(x, 6) for x in soundfile.at_percent(0.21)],
            0.41: [round(x, 6) for x in soundfile.at_percent(0.41)],
            0.61: [round(x, 6) for x in soundfile.at_percent(0.61)],
            0.81: [round(x, 6) for x in soundfile.at_percent(0.81)],
            0.99: [round(x, 6) for x in soundfile.at_percent(0.99)],
            }

    def test_01a(self):
        """
        Default Session IO counts: 8x8
        """
        session = self._make_session(input_bus_channel_count=None, output_bus_channel_count=None)
        exit_code, _ = session.render(self.output_filepath)
        self.assert_ok(exit_code, 10., 44100, 8)
        assert self._sample(self.output_filepath) == {
            0.0: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            0.41: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            0.61: [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            0.81: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            0.99: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            }

    def test_01b(self):
        """
        Overriden pre-render Session IO counts: 0x2

        Should be reflected in resulting soundfile.
        """
        session = self._make_session(input_bus_channel_count=0, output_bus_channel_count=2)
        exit_code, _ = session.render(self.output_filepath)
        self.assert_ok(exit_code, 10., 44100, 2)
        assert self._sample(self.output_filepath) == {
            0.0: [0.0, 0.0],
            0.21: [0.25, 0.25],
            0.41: [0.5, 0.5],
            0.61: [0.75, 0.75],
            0.81: [1.0, 1.0],
            0.99: [1.0, 1.0],
            }

    def test_01c(self):
        """
        Overriden pre-render Session IO counts: 0x2
        Overriden post-render Session IO counts: 4x4

        Post-render counts should be reflected in resulting soundfile.
        """
        session = self._make_session(input_bus_channel_count=0, output_bus_channel_count=2)
        exit_code, _ = session.render(
            self.output_filepath,
            input_bus_channel_count=4,
            output_bus_channel_count=4,
            )
        self.assert_ok(exit_code, 10., 44100, 4)
        assert self._sample(self.output_filepath) == {
            0.0: [0.0, 0.0, 0.0, 0.0],
            0.21: [0.25, 0.25, 0.0, 0.0],
            0.41: [0.5, 0.5, 0.0, 0.0],
            0.61: [0.75, 0.75, 0.0, 0.0],
            0.81: [1.0, 1.0, 0.0, 0.0],
            0.99: [1.0, 1.0, 0.0, 0.0],
            }

    def test_02a(self):
        """
        Soundfile NRT input, unprocessed.
        """
        output_one = os.path.join(self.output_directory, 'output-one.aiff')
        output_two = os.path.join(self.output_directory, 'output-two.aiff')
        self.output_filepaths.extend([output_one, output_two])
        # Session One
        session_one = self._make_session(output_bus_channel_count=1)
        exit_code, _ = session_one.render(output_one)
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_one)
        assert self._sample(output_one) == {
            0.0: [0.0],
            0.21: [0.25],
            0.41: [0.5],
            0.61: [0.75],
            0.81: [1.0],
            0.99: [1.0],
            }
        # Session Two
        session_two = nonrealtimetools.Session(
            input_bus_channel_count=1,
            output_bus_channel_count=1,
            )
        exit_code, _ = session_two.render(
            output_two,
            input_filename=output_one,
            duration=10.,
            )
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_two)
        assert self._sample(output_two) == {
            0.0: [0.0],
            0.21: [0.0],
            0.41: [0.0],
            0.61: [0.0],
            0.81: [0.0],
            0.99: [0.0],
            }

    def test_02b(self):
        """
        Soundfile NRT input, pass-through processing.
        """
        output_one = os.path.join(self.output_directory, 'output-one.aiff')
        output_two = os.path.join(self.output_directory, 'output-two.aiff')
        self.output_filepaths.extend([output_one, output_two])
        # Session One
        session_one = self._make_session(output_bus_channel_count=1)
        exit_code, _ = session_one.render(output_one)
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_one)
        assert self._sample(output_one) == {
            0.0: [0.0],
            0.21: [0.25],
            0.41: [0.5],
            0.61: [0.75],
            0.81: [1.0],
            0.99: [1.0],
            }
        # Session Two
        session_two = nonrealtimetools.Session(
            input_bus_channel_count=1,
            output_bus_channel_count=1,
            )
        synthdef = self.build_multiplier_synthdef()
        with session_two.at(0):
            session_two.add_synth(
                duration=10,
                in_bus=session_two.audio_input_bus_group,
                multiplier=1,
                out_bus=session_two.audio_output_bus_group,
                synthdef=synthdef,
                )
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '13638b770593ac9834eac8f150ad986a', 1000, 0, 0,
                    'in_bus', 1, 'multiplier', 1, 'out_bus', 0]]],
            [10.0, [['/n_free', 1000], [0]]]]
        exit_code, _ = session_two.render(
            output_two,
            input_filename=output_one,
            duration=10.,
            )
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_two)
        assert self._sample(output_two) == {
            0.0: [0.0],
            0.21: [0.25],
            0.41: [0.5],
            0.61: [0.75],
            0.81: [1.0],
            0.99: [1.0],
            }

    def test_02c(self):
        """
        Soundfile NRT input, processed.
        """
        output_one = os.path.join(self.output_directory, 'output-one.aiff')
        output_two = os.path.join(self.output_directory, 'output-two.aiff')
        self.output_filepaths.extend([output_one, output_two])
        # Session One
        session_one = self._make_session(output_bus_channel_count=1)
        exit_code, _ = session_one.render(output_one)
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_one)
        assert self._sample(output_one) == {
            0.0: [0.0],
            0.21: [0.25],
            0.41: [0.5],
            0.61: [0.75],
            0.81: [1.0],
            0.99: [1.0],
            }
        # Session Two
        session_two = nonrealtimetools.Session(
            input_bus_channel_count=1,
            output_bus_channel_count=1,
            )
        synthdef = self.build_multiplier_synthdef()
        with session_two.at(0):
            session_two.add_synth(
                duration=10,
                in_bus=session_two.audio_input_bus_group,
                multiplier=-0.5,
                out_bus=session_two.audio_output_bus_group,
                synthdef=synthdef,
                )
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '13638b770593ac9834eac8f150ad986a', 1000, 0, 0,
                    'in_bus', 1, 'multiplier', -0.5, 'out_bus', 0]]],
            [10.0, [['/n_free', 1000], [0]]]]
        exit_code, _ = session_two.render(
            output_two,
            input_filename=output_one,
            duration=10.,
            )
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_two)
        assert self._sample(output_two) == {
            0.0: [0.0],
            0.21: [-0.125],
            0.41: [-0.25],
            0.61: [-0.375],
            0.81: [-0.5],
            0.99: [-0.5],
            }

    def test_02d(self):
        """
        Soundfile NRT input, processed, differing channel counts.
        """
        output_one = os.path.join(self.output_directory, 'output-one.aiff')
        output_two = os.path.join(self.output_directory, 'output-two.aiff')
        self.output_filepaths.extend([output_one, output_two])
        # Session One
        session_one = self._make_session(output_bus_channel_count=1)
        exit_code, _ = session_one.render(output_one)
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_one)
        assert self._sample(output_one) == {
            0.0: [0.0],
            0.21: [0.25],
            0.41: [0.5],
            0.61: [0.75],
            0.81: [1.0],
            0.99: [1.0],
            }
        # Session Two
        session_two = nonrealtimetools.Session(
            input_bus_channel_count=1,
            output_bus_channel_count=2,
            )
        synthdef = self.build_multiplier_synthdef(channel_count=1)
        with session_two.at(0):
            session_two.add_synth(
                duration=10,
                in_bus=session_two.audio_input_bus_group,
                multiplier=-0.5,
                out_bus=session_two.audio_output_bus_group,
                synthdef=synthdef,
                )
        assert session_two.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '13638b770593ac9834eac8f150ad986a', 1000, 0, 0,
                    'in_bus', 2, 'multiplier', -0.5, 'out_bus', 0]]],
            [10.0, [['/n_free', 1000], [0]]]]
        exit_code, _ = session_two.render(
            output_two,
            input_filename=output_one,
            duration=10.,
            )
        self.assert_ok(exit_code, 10., 44100, 2, filepath=output_two)
        assert self._sample(output_two) == {
            0.0: [0.0, 0.0],
            0.21: [-0.125, 0.0],
            0.41: [-0.25, 0.0],
            0.61: [-0.375, 0.0],
            0.81: [-0.5, 0.0],
            0.99: [-0.5, 0.0],
            }

    def test_03(self):
        """
        Soundfile DiskIn input.
        """
        output_one = os.path.join(self.output_directory, 'output-one.aiff')
        output_two = os.path.join(self.output_directory, 'output-two.aiff')
        self.output_filepaths.extend([output_one, output_two])
        # Session One
        session_one = self._make_session(output_bus_channel_count=1)
        exit_code, _ = session_one.render(output_one)
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_one)
        # Session Two
        session_two = nonrealtimetools.Session(
            input_bus_channel_count=1,
            output_bus_channel_count=1,
            )
        synthdef = self.build_diskin_synthdef(channel_count=1)
        with session_two.at(0):
            buffer_ = session_two.cue_soundfile(
                output_one,
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
                ['/b_alloc', 0, 32768, 1],
                ['/b_read', 0, output_one, 0, -1, 0, 1],
                ['/s_new', '9c69c44ff72c62dfa4c2f0a0e99f05ce', 1000, 0, 0,
                    'buffer_id', 0]]],
            [10.0, [
                ['/n_free', 1000],
                ['/b_close', 0],
                ['/b_free', 0], [0]]]]
        exit_code, _ = session_two.render(output_two, duration=10.)
        self.assert_ok(exit_code, 10., 44100, 1, filepath=output_two)
        assert self._sample(output_one) == {
            0.0: [0.0],
            0.21: [0.25],
            0.41: [0.5],
            0.61: [0.75],
            0.81: [1.0],
            0.99: [1.0],
            }

    @unittest.skip('TODO')
    def test_04(self):
        """
        Session DiskIn input.
        """

    @unittest.skip('TODO')
    def test_05(self):
        """
        Session NRT input.
        """

    @unittest.skip('TODO')
    def test_07(self):
        """
        Chained Session NRT input.
        """
