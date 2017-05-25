# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from supriya import SynthDefFactory
from supriya import ugentools


class TestCase(systemtools.TestCase):

    def test_gate_01(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = SynthDefFactory(channel_count=1)
        factory = factory.with_signal_block(signal_block)
        factory = factory.with_gate()
        factory = factory.with_output()
        self.compare_strings('''
        SynthDef 937f9dd172e0c2ec52916ce2ae4cb9c1 {
            1_TrigControl[0:gate] -> 2_Linen[0:gate]
            const_0:0.02 -> 2_Linen[1:attack_time]
            const_1:1.0 -> 2_Linen[2:sustain_level]
            const_0:0.02 -> 2_Linen[3:release_time]
            const_2:2.0 -> 2_Linen[4:done_action]
            const_3:440.0 -> 3_SinOsc[0:frequency]
            const_4:0.0 -> 3_SinOsc[1:phase]
            3_SinOsc[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            2_Linen[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            0_Control[0:out] -> 5_Out[0:bus]
            4_BinaryOpUGen:MULTIPLICATION[0] -> 5_Out[1:source]
        }
        ''', str(factory.build()))

    def test_gate_02(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = SynthDefFactory(channel_count=1)
        factory = factory.with_signal_block(signal_block)
        factory = factory.with_gate()
        factory = factory.with_output(
            crossfaded=True,
            )
        self.compare_strings('''
        SynthDef b2b4641122aa7170a652c245e97f995e {
            1_TrigControl[0:gate] -> 2_Linen[0:gate]
            const_0:0.02 -> 2_Linen[1:attack_time]
            const_1:1.0 -> 2_Linen[2:sustain_level]
            const_0:0.02 -> 2_Linen[3:release_time]
            const_2:2.0 -> 2_Linen[4:done_action]
            3_Control[0:crossfade] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            2_Linen[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            const_3:440.0 -> 5_SinOsc[0:frequency]
            const_4:0.0 -> 5_SinOsc[1:phase]
            0_Control[0:out] -> 6_XOut[0:bus]
            4_BinaryOpUGen:MULTIPLICATION[0] -> 6_XOut[1:crossfade]
            5_SinOsc[0] -> 6_XOut[2:source]
        }
        ''', str(factory.build()))

    def test_gate_03(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = SynthDefFactory(channel_count=1)
        factory = factory.with_signal_block(signal_block)
        factory = factory.with_gate()
        factory = factory.with_output(
            crossfaded=True,
            windowed=True,
            )
        self.compare_strings('''
        SynthDef 7758ec85f0a5e78d07ac88e6e9ac17db {
            const_0:0.0 -> 1_Line[0:start]
            const_1:1.0 -> 1_Line[1:stop]
            0_Control[0:duration] -> 1_Line[2:duration]
            const_2:2.0 -> 1_Line[3:done_action]
            1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
            3_TrigControl[0:gate] -> 4_Linen[0:gate]
            const_3:0.02 -> 4_Linen[1:attack_time]
            const_1:1.0 -> 4_Linen[2:sustain_level]
            const_3:0.02 -> 4_Linen[3:release_time]
            const_2:2.0 -> 4_Linen[4:done_action]
            2_UnaryOpUGen:HANNING_WINDOW[0] -> 5_BinaryOpUGen:MULTIPLICATION[0:left]
            4_Linen[0] -> 5_BinaryOpUGen:MULTIPLICATION[1:right]
            const_4:440.0 -> 6_SinOsc[0:frequency]
            const_0:0.0 -> 6_SinOsc[1:phase]
            0_Control[1:out] -> 7_XOut[0:bus]
            5_BinaryOpUGen:MULTIPLICATION[0] -> 7_XOut[1:crossfade]
            6_SinOsc[0] -> 7_XOut[2:source]
        }
        ''', str(factory.build()))

    def test_gate_04(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = SynthDefFactory(channel_count=1)
        factory = factory.with_signal_block(signal_block)
        factory = factory.with_gate()
        factory = factory.with_output(
            crossfaded=True,
            leveled=True,
            windowed=True,
            )
        self.compare_strings('''
        SynthDef 976b3fc57d1862cb178148b04472e51c {
            const_0:0.0 -> 1_Line[0:start]
            const_1:1.0 -> 1_Line[1:stop]
            0_Control[0:duration] -> 1_Line[2:duration]
            const_2:2.0 -> 1_Line[3:done_action]
            1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
            3_TrigControl[0:gate] -> 4_Linen[0:gate]
            const_3:0.02 -> 4_Linen[1:attack_time]
            const_1:1.0 -> 4_Linen[2:sustain_level]
            const_3:0.02 -> 4_Linen[3:release_time]
            const_2:2.0 -> 4_Linen[4:done_action]
            2_UnaryOpUGen:HANNING_WINDOW[0] -> 6_BinaryOpUGen:MULTIPLICATION[0:left]
            5_Control[0:level] -> 6_BinaryOpUGen:MULTIPLICATION[1:right]
            6_BinaryOpUGen:MULTIPLICATION[0] -> 7_BinaryOpUGen:MULTIPLICATION[0:left]
            4_Linen[0] -> 7_BinaryOpUGen:MULTIPLICATION[1:right]
            const_4:440.0 -> 8_SinOsc[0:frequency]
            const_0:0.0 -> 8_SinOsc[1:phase]
            0_Control[1:out] -> 9_XOut[0:bus]
            7_BinaryOpUGen:MULTIPLICATION[0] -> 9_XOut[1:crossfade]
            8_SinOsc[0] -> 9_XOut[2:source]
        }
        ''', str(factory.build()))
