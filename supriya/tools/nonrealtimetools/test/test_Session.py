# -*- encoding: utf-8 -*-
from supriya.tools import nonrealtimetools
from supriya.tools import osctools
from supriya.tools import soundfiletools
from supriya.tools.nonrealtimetools.TestCase import TestCase


class TestCase(TestCase):

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

    def test_04(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.build_duration_synthdef(),
                )
        assert session.to_osc_bundles() == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 448a8d487adfc99ec697033edc2a1227\x00\x00\x00\x02\x00\x00\x00\x00?\x80\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x08duration\x00\x00\x00\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x04Line\x02\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1000, 0, 0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.0,
                contents=(
                    osctools.OscMessage('/n_free', 1000),
                    osctools.OscMessage(0),
                    )
                ),
            ]
        exit_code, _ = session.render(
            self.output_filepath,
            output_bus_channel_count=1,
            )
        self.assert_ok(exit_code, 1., 44100, 1)
        soundfile = soundfiletools.SoundFile(self.output_filepath)
        for i in range(1, 100):
            value = float(i) / 100
            #print(i, value, self.round(soundfile.at_percent(value)[0]))
            assert self.round(soundfile.at_percent(value)[0]) == value

    def test_05(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.build_gate_synthdef(),
                )
        assert session.to_osc_bundles(duration=2) == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 fc663c6d1f8badaed1bd3e25cf2220f0\x00\x00\x00\x08?\x80\x00\x00\x00\x00\x00\x00@\x00\x00\x00\xc2\xc6\x00\x00<#\xd7\n@\xa0\x00\x00\xc0\x80\x00\x00C\xdc\x00\x00\x00\x00\x00\x01?\x80\x00\x00\x00\x00\x00\x01\x04gate\x00\x00\x00\x00\x00\x00\x00\x05\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x06EnvGen\x02\x00\x00\x00\x11\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x06\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x06\x02\x03Saw\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x07\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', 'fc663c6d1f8badaed1bd3e25cf2220f0', 1000, 0, 0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.0,
                contents=(
                    osctools.OscMessage('/n_set', 1000, 'gate', 0),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.0,
                contents=(
                    osctools.OscMessage(0),
                    )
                ),
            ]
