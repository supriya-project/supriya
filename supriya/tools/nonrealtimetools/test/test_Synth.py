# -*- encoding: utf-8 -*-
import os
import unittest
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
        session = nonrealtimetools.Session()
        synth_one = session.add_synth(
            0, 4,
            synthdef=self.build_synthdef(),
            )
        synth_two = session.add_synth(
            2, 6,
            synthdef=self.build_synthdef(),
            frequency=330,
            )

        with session.at(2):
            synth_one['frequency'] = 550
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
            assert synth_two['frequency'] == 330
        with session.at(3):
            assert synth_one['frequency'] == 660
            assert synth_two['frequency'] == 770
        with session.at(4):
            assert synth_two['frequency'] == 880
        with session.at(5):
            assert synth_two['frequency'] == 880