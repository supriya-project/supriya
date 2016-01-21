# -*- encoding: utf-8 -*-
import os
import unittest
from abjad.tools import timespantools
from supriya.tools import nonrealtimetools
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

    def test_01(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.build_basic_synthdef(),
                )
        exit_code, _ = session.render(self.output_filepath)
        self.assert_ok(exit_code, 1., 44100, 8)

    def test_02(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(
                duration=300,
                synthdef=self.build_basic_synthdef(),
                )
        exit_code, _ = session.render(
            self.output_filepath,
            sample_rate=48000,
            output_bus_channel_count=2,
            )
        self.assert_ok(exit_code, 300., 48000, 2)

    def test_03(self):
        session = nonrealtimetools.Session()
        with session.at(1):
            session.add_synth(
                duration=2,
                synthdef=self.build_basic_synthdef(),
                )
        timespan = timespantools.Timespan(0.5, 2.5)
        assert session.to_osc_bundles(timespan=timespan) == [
            osctools.OscBundle(
                timestamp=0.5,
                contents=[
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 d719856d7deff2696a3f807f5dc79809\x00\x00\x00\x02C\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', 'd719856d7deff2696a3f807f5dc79809', 1000, 1, 0),
                    ]
                ),
            osctools.OscBundle(
                timestamp=1.5,
                contents=[osctools.OscMessage('/n_free', 1000)]
                ),
            osctools.OscBundle(
                timestamp=2.5,
                contents=[osctools.OscMessage(0)]
                ),
            ]

    def test_04(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.build_duration_synthdef(),
                )
        exit_code, _ = session.render(
            self.output_filepath,
            output_bus_channel_count=1,
            )
        self.assert_ok(exit_code, 1., 44100, 1)
        soundfile = soundfiletools.SoundFile(self.output_filepath)
        for i in range(1, 100):
            value = float(i) / 100
            assert self.round(soundfile.at_percent(value)[0]) == value

    def test_05(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.build_gate_synthdef(),
                )
        timespan = timespantools.Timespan(0, 3)
        assert session.to_osc_bundles(timespan=timespan) == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 fc663c6d1f8badaed1bd3e25cf2220f0\x00\x00\x00\x08?\x80\x00\x00\x00\x00\x00\x00@\x00\x00\x00\xc2\xc6\x00\x00<#\xd7\n@\xa0\x00\x00\xc0\x80\x00\x00C\xdc\x00\x00\x00\x00\x00\x01?\x80\x00\x00\x00\x00\x00\x01\x04gate\x00\x00\x00\x00\x00\x00\x00\x05\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x06EnvGen\x02\x00\x00\x00\x11\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x06\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x06\x02\x03Saw\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x07\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', 'fc663c6d1f8badaed1bd3e25cf2220f0', 1000, 1, 0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.0,
                contents=(
                    osctools.OscMessage('/n_set', 1000, 'gate', 0),
                    )
                ),
            osctools.OscBundle(
                timestamp=3.0,
                contents=(
                    osctools.OscMessage(0),
                    )
                ),
            ]
