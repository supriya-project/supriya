# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from supriya import DoneAction, Parameter, SynthDefBuilder, SynthDefFactory
from supriya import synthdeftools
from supriya import ugentools


class TestCase(systemtools.TestCase):

    def test_01(self):
        def build_synthdef_manually():
            channel_count = 2
            with SynthDefBuilder(
                duration=Parameter(parameter_rate='SCALAR', value=1),
                level=1.0,
                out=Parameter(parameter_rate='SCALAR', value=0),
                ) as builder:
                window = ugentools.Line.kr(
                    done_action=2,
                    duration=builder['duration'],
                    ).hanning_window()
                source = ugentools.In.ar(
                    bus=builder['out'],
                    channel_count=channel_count,
                    )
                maximum_delay = ugentools.Rand.ir(0.1, 1)
                allpasses = []
                for output in source:
                    for _ in range(3):
                        output = ugentools.AllpassC.ar(
                            decay_time=ugentools.LFDNoise3.kr(
                                frequency=ugentools.ExpRand.ir(0.01, 0.1),
                                ).scale(-1, 1, 0.001, 1),
                            delay_time=ugentools.LFDNoise3.kr(
                                frequency=ugentools.ExpRand.ir(0.01, 0.1),
                                ).scale(-1, 1, 0.001, 1) * maximum_delay,
                            maximum_delay_time=maximum_delay,
                            source=output,
                            )
                    allpasses.append(output)
                source = synthdeftools.UGenArray(allpasses)
                ugentools.XOut.ar(
                    bus=builder['out'],
                    crossfade=window,
                    source=source * builder['level'],
                    )
            return builder.build()

        def signal_block(builder, source, state):
            maximum_delay = ugentools.Rand.ir(0.1, 1)
            allpasses = []
            for output in source:
                for _ in range(3):
                    output = ugentools.AllpassC.ar(
                        decay_time=ugentools.LFDNoise3.kr(
                            frequency=ugentools.ExpRand.ir(0.01, 0.1),
                            ).scale(-1, 1, 0.001, 1),
                        delay_time=ugentools.LFDNoise3.kr(
                            frequency=ugentools.ExpRand.ir(0.01, 0.1),
                            ).scale(-1, 1, 0.001, 1) * maximum_delay,
                        maximum_delay_time=maximum_delay,
                        source=output,
                        )
                allpasses.append(output)
            return synthdeftools.UGenArray(allpasses)

        factory = SynthDefFactory(channel_count=2)
        factory = factory.with_input()
        factory = factory.with_output(crossfaded=True, leveled=True, windowed=True)
        factory = factory.with_signal_block(signal_block)
        factory_synthdef = factory.build()
        manual_synthdef = build_synthdef_manually()
        self.compare_strings(str(manual_synthdef), str(factory_synthdef))

    def test_02(self):
        def build_synthdef_manually():
            channel_count = 2
            with SynthDefBuilder(
                duration=Parameter(parameter_rate='SCALAR', value=1),
                level=1.0,
                out=Parameter(parameter_rate='SCALAR', value=0),
                ) as builder:
                window = ugentools.Line.kr(
                    done_action=2,
                    duration=builder['duration'],
                    ).hanning_window()
                source = ugentools.In.ar(
                    bus=builder['out'],
                    channel_count=channel_count,
                    )
                source += ugentools.LocalIn.ar(channel_count=channel_count)
                source *= ugentools.Line.kr(duration=0.1)
                allpasses = []
                maximum_delay = ugentools.Rand.ir(0.1, 1)
                for output in source:
                    for _ in range(3):
                        output = ugentools.AllpassC.ar(
                            decay_time=ugentools.LFDNoise3.kr(
                                frequency=ugentools.ExpRand.ir(0.01, 0.1),
                                ).scale(-1, 1, 0.001, 1),
                            delay_time=ugentools.LFDNoise3.kr(
                                frequency=ugentools.ExpRand.ir(0.01, 0.1),
                                ).scale(-1, 1, 0.001, 1) * maximum_delay,
                            maximum_delay_time=maximum_delay,
                            source=output,
                            )
                    allpasses.append(output)
                source = synthdeftools.UGenArray(allpasses)
                source = ugentools.LeakDC.ar(source=source)
                source = ugentools.Limiter.ar(source=source)
                ugentools.XOut.ar(
                    bus=builder['out'],
                    crossfade=window,
                    source=source * builder['level'],
                    )
                ugentools.LocalOut.ar(
                    source=source * -0.9 * ugentools.LFDNoise1.kr(frequency=0.1)
                    )
                ugentools.DetectSilence.kr(
                    done_action=DoneAction.FREE_SYNTH,
                    source=ugentools.Mix.new(source),
                    )
                return builder.build()

        def feedback_loop(builder, source, state):
            return source * -0.9 * ugentools.LFDNoise1.kr(frequency=0.1)

        def signal_block_one(builder, source, state):
            source *= ugentools.Line.kr(duration=0.1)
            maximum_delay = ugentools.Rand.ir(0.1, 1)
            allpasses = []
            for output in source:
                for _ in range(3):
                    output = ugentools.AllpassC.ar(
                        decay_time=ugentools.LFDNoise3.kr(
                            frequency=ugentools.ExpRand.ir(0.01, 0.1),
                            ).scale(-1, 1, 0.001, 1),
                        delay_time=ugentools.LFDNoise3.kr(
                            frequency=ugentools.ExpRand.ir(0.01, 0.1),
                            ).scale(-1, 1, 0.001, 1) * maximum_delay,
                        maximum_delay_time=maximum_delay,
                        source=output,
                        )
                allpasses.append(output)
            return synthdeftools.UGenArray(allpasses)

        def signal_block_two(builder, source, state):
            source = ugentools.LeakDC.ar(source=source)
            source = ugentools.Limiter.ar(source=source)
            return source

        factory = SynthDefFactory(channel_count=2)
        factory = factory.with_feedback_loop(feedback_loop)
        factory = factory.with_input()
        factory = factory.with_output(crossfaded=True, leveled=True, windowed=True)
        factory = factory.with_signal_block(signal_block_one)
        factory = factory.with_signal_block(signal_block_two)
        factory = factory.with_silence_detection()
        factory_synthdef = factory.build()
        manual_synthdef = build_synthdef_manually()
        self.compare_strings(str(manual_synthdef), str(factory_synthdef))

    def test_gate_01(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = SynthDefFactory(channel_count=1)
        factory = factory.with_signal_block(signal_block)
        factory = factory.with_gate()
        factory = factory.with_output()
        self.compare_strings('''
        SynthDef 937f9dd172e0c2ec52916ce2ae4cb9c1 {
            1_TrigControl[0] -> 2_Linen[0:gate]
            const_0:0.02 -> 2_Linen[1:attack_time]
            const_1:1.0 -> 2_Linen[2:sustain_level]
            const_0:0.02 -> 2_Linen[3:release_time]
            const_2:2.0 -> 2_Linen[4:done_action]
            const_3:440.0 -> 3_SinOsc[0:frequency]
            const_4:0.0 -> 3_SinOsc[1:phase]
            3_SinOsc[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            2_Linen[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            0_Control[0] -> 5_Out[0:bus]
            4_BinaryOpUGen:MULTIPLICATION[0] -> 5_Out[1:source]
        }
        ''', str(factory.build()))

    def test_gate_02(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = SynthDefFactory(channel_count=1)
        factory = factory.with_signal_block(signal_block)
        factory = factory.with_gate()
        factory = factory.with_output(crossfaded=True)
        self.compare_strings('''
        SynthDef b2b4641122aa7170a652c245e97f995e {
            1_TrigControl[0] -> 2_Linen[0:gate]
            const_0:0.02 -> 2_Linen[1:attack_time]
            const_1:1.0 -> 2_Linen[2:sustain_level]
            const_0:0.02 -> 2_Linen[3:release_time]
            const_2:2.0 -> 2_Linen[4:done_action]
            3_Control[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            2_Linen[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            const_3:440.0 -> 5_SinOsc[0:frequency]
            const_4:0.0 -> 5_SinOsc[1:phase]
            0_Control[0] -> 6_XOut[0:bus]
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
        factory = factory.with_output(crossfaded=True, windowed=True)
        self.compare_strings('''
        SynthDef 7758ec85f0a5e78d07ac88e6e9ac17db {
            const_0:0.0 -> 1_Line[0:start]
            const_1:1.0 -> 1_Line[1:stop]
            0_Control[0] -> 1_Line[2:duration]
            const_2:2.0 -> 1_Line[3:done_action]
            1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
            3_TrigControl[0] -> 4_Linen[0:gate]
            const_3:0.02 -> 4_Linen[1:attack_time]
            const_1:1.0 -> 4_Linen[2:sustain_level]
            const_3:0.02 -> 4_Linen[3:release_time]
            const_2:2.0 -> 4_Linen[4:done_action]
            2_UnaryOpUGen:HANNING_WINDOW[0] -> 5_BinaryOpUGen:MULTIPLICATION[0:left]
            4_Linen[0] -> 5_BinaryOpUGen:MULTIPLICATION[1:right]
            const_4:440.0 -> 6_SinOsc[0:frequency]
            const_0:0.0 -> 6_SinOsc[1:phase]
            0_Control[1] -> 7_XOut[0:bus]
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
        factory = factory.with_output(crossfaded=True, leveled=True, windowed=True)
        self.compare_strings('''
        SynthDef 077c1d5506728cf41d5c1c250059894d {
            const_0:0.0 -> 1_Line[0:start]
            const_1:1.0 -> 1_Line[1:stop]
            0_Control[0] -> 1_Line[2:duration]
            const_2:2.0 -> 1_Line[3:done_action]
            1_Line[0] -> 2_UnaryOpUGen:HANNING_WINDOW[0:source]
            3_TrigControl[0] -> 4_Linen[0:gate]
            const_3:0.02 -> 4_Linen[1:attack_time]
            const_1:1.0 -> 4_Linen[2:sustain_level]
            const_3:0.02 -> 4_Linen[3:release_time]
            const_2:2.0 -> 4_Linen[4:done_action]
            2_UnaryOpUGen:HANNING_WINDOW[0] -> 5_BinaryOpUGen:MULTIPLICATION[0:left]
            4_Linen[0] -> 5_BinaryOpUGen:MULTIPLICATION[1:right]
            const_4:440.0 -> 7_SinOsc[0:frequency]
            const_0:0.0 -> 7_SinOsc[1:phase]
            7_SinOsc[0] -> 8_BinaryOpUGen:MULTIPLICATION[0:left]
            6_Control[0] -> 8_BinaryOpUGen:MULTIPLICATION[1:right]
            0_Control[1] -> 9_XOut[0:bus]
            5_BinaryOpUGen:MULTIPLICATION[0] -> 9_XOut[1:crossfade]
            8_BinaryOpUGen:MULTIPLICATION[0] -> 9_XOut[2:source]
        }
        ''', str(factory.build()))
