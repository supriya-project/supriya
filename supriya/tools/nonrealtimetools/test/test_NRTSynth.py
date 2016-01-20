# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import durationtools
from supriya.tools import nonrealtimetools
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(unittest.TestCase):

    def build_synthdef(self):
        builder = synthdeftools.SynthDefBuilder(
            frequency=440,
            amplitude=1.,
            in_bus=0,
            out_bus=2,
            )
        with builder:
            input_ = ugentools.In.ar(bus=builder['in_bus'])
            source = ugentools.SinOsc.ar(frequency=builder['frequency'])
            source *= builder['amplitude']
            source *= input_
            ugentools.Out.ar(
                bus=builder['out_bus'],
                source=source,
                )
        return builder.build()

    def test_01(self):
        session = nonrealtimetools.NRTSession()
        with session.at(0):
            synth_one = session.add_synth(
                duration=4,
                synthdef=self.build_synthdef(),
                )
        with session.at(2):
            synth_two = session.add_synth(
                duration=6,
                synthdef=self.build_synthdef(),
                frequency=330,
                )

        with session.at(2):
            synth_one['frequency'] = 550
            synth_two['frequency'] = 333
        with session.at(3):
            synth_one['frequency'] = 660
            synth_two['frequency'] = 770
        with session.at(4):
            synth_two['frequency'] = 880

        with session.at(0):
            assert synth_one['frequency'] == 440
        with session.at(1):
            assert synth_one['frequency'] == 440
        with session.at(2):
            assert synth_one['frequency'] == 550
            assert synth_two['frequency'] == 333
        with session.at(3):
            assert synth_one['frequency'] == 660
            assert synth_two['frequency'] == 770
        with session.at(4):
            assert synth_two['frequency'] == 880
        with session.at(5):
            assert synth_two['frequency'] == 880
