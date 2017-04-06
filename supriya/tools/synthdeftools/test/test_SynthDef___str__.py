# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from supriya import synthdeftools
from supriya import ugentools


class TestCase(systemtools.TestCase):

    def test_multi_value_parameters(self):
        with synthdeftools.SynthDefBuilder(
            amp=0.1,
            freqs=[300, 400],
            out=0,
            ) as builder:
            sines = ugentools.SinOsc.ar(
                frequency=builder['freqs'],
                )
            sines = ugentools.Mix.new(sines)
            sines = sines * builder['amp']
            ugentools.Out.ar(
                bus=builder['out'],
                source=sines,
                )
        synthdef = builder.build()
        self.compare_strings(
            '''
            SynthDef ... {
                0_Control[1:freqs[0]] -> 1_SinOsc[0:frequency]
                const_0:0.0 -> 1_SinOsc[1:phase]
                0_Control[2:freqs[1]] -> 2_SinOsc[0:frequency]
                const_0:0.0 -> 2_SinOsc[1:phase]
                1_SinOsc[0] -> 3_BinaryOpUGen:ADDITION[0:left]
                2_SinOsc[0] -> 3_BinaryOpUGen:ADDITION[1:right]
                3_BinaryOpUGen:ADDITION[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
                0_Control[0:amp] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
                0_Control[3:out] -> 5_Out[0:bus]
                4_BinaryOpUGen:MULTIPLICATION[0] -> 5_Out[1:source]
            }
            ''',
            str(synthdef),
            )
