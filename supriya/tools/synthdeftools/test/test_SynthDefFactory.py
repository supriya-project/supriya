# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from supriya import DoneAction, SynthDefBuilder
from supriya import synthdeftools
from supriya import ugentools


class TestCase(systemtools.TestCase):

    def test_01(self):
        def build_synthdef_manually():
            channel_count = 2
            with SynthDefBuilder(duration=1.0, level=1.0, out=0) as builder:
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

        factory = synthdeftools.SynthDefFactory(channel_count=2)
        factory.with_input()
        factory.with_output(crossfaded=True, leveled=True, windowed=True)
        factory.with_signal_block(signal_block)
        factory_synthdef = factory.build()
        manual_synthdef = build_synthdef_manually()
        self.compare_strings(str(manual_synthdef), str(factory_synthdef))

    def test_02(self):
        def build_synthdef_manually():
            channel_count = 2
            with SynthDefBuilder(duration=1.0, level=1.0, out=0) as builder:
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

        factory = synthdeftools.SynthDefFactory(channel_count=2)
        factory.with_feedback_loop(feedback_loop)
        factory.with_input()
        factory.with_output(crossfaded=True, leveled=True, windowed=True)
        factory.with_signal_block(signal_block_one)
        factory.with_signal_block(signal_block_two)
        factory.with_silence_detection()
        factory_synthdef = factory.build()
        manual_synthdef = build_synthdef_manually()
        self.compare_strings(str(manual_synthdef), str(factory_synthdef))

    def test_gate_01(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = synthdeftools.SynthDefFactory(channel_count=1)
        factory.with_signal_block(signal_block)
        factory.with_gate()
        factory.with_output()
        self.compare_strings('''
        SynthDef 6e93b495036d8170d2f849155816514c {
            0_Control[0] -> 1_Linen[0:gate]
            const_0:0.02 -> 1_Linen[1:attack_time]
            const_1:1.0 -> 1_Linen[2:sustain_level]
            const_0:0.02 -> 1_Linen[3:release_time]
            const_2:2.0 -> 1_Linen[4:done_action]
            const_3:440.0 -> 2_SinOsc[0:frequency]
            const_4:0.0 -> 2_SinOsc[1:phase]
            2_SinOsc[0] -> 3_BinaryOpUGen:MULTIPLICATION[0:left]
            1_Linen[0] -> 3_BinaryOpUGen:MULTIPLICATION[1:right]
            0_Control[1] -> 4_Out[0:bus]
            3_BinaryOpUGen:MULTIPLICATION[0] -> 4_Out[1:source]
        }
        ''', str(factory.build()))

    def test_gate_02(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = synthdeftools.SynthDefFactory(channel_count=1)
        factory.with_signal_block(signal_block)
        factory.with_gate()
        factory.with_output(crossfaded=True)
        self.compare_strings('''
        SynthDef cb1639f20065ae9c58cc712d84dc68f4 {
            0_Control[1] -> 1_Linen[0:gate]
            const_0:0.02 -> 1_Linen[1:attack_time]
            const_1:1.0 -> 1_Linen[2:sustain_level]
            const_0:0.02 -> 1_Linen[3:release_time]
            const_2:2.0 -> 1_Linen[4:done_action]
            0_Control[0] -> 2_BinaryOpUGen:MULTIPLICATION[0:left]
            1_Linen[0] -> 2_BinaryOpUGen:MULTIPLICATION[1:right]
            const_3:440.0 -> 3_SinOsc[0:frequency]
            const_4:0.0 -> 3_SinOsc[1:phase]
            0_Control[2] -> 4_XOut[0:bus]
            2_BinaryOpUGen:MULTIPLICATION[0] -> 4_XOut[1:crossfade]
            3_SinOsc[0] -> 4_XOut[2:source]
        }
        ''', str(factory.build()))

    def test_gate_03(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = synthdeftools.SynthDefFactory(channel_count=1)
        factory.with_signal_block(signal_block)
        factory.with_gate()
        factory.with_output(crossfaded=True, windowed=True)
        self.compare_strings('''
        SynthDef 23408f76776475102e54776932465d59 {
            0_Control[1] -> 1_Linen[0:gate]
            const_0:0.02 -> 1_Linen[1:attack_time]
            const_1:1.0 -> 1_Linen[2:sustain_level]
            const_0:0.02 -> 1_Linen[3:release_time]
            const_2:2.0 -> 1_Linen[4:done_action]
            const_3:0.0 -> 2_Line[0:start]
            const_1:1.0 -> 2_Line[1:stop]
            0_Control[0] -> 2_Line[2:duration]
            const_2:2.0 -> 2_Line[3:done_action]
            2_Line[0] -> 3_UnaryOpUGen:HANNING_WINDOW[0:source]
            3_UnaryOpUGen:HANNING_WINDOW[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            1_Linen[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            const_4:440.0 -> 5_SinOsc[0:frequency]
            const_3:0.0 -> 5_SinOsc[1:phase]
            0_Control[2] -> 6_XOut[0:bus]
            4_BinaryOpUGen:MULTIPLICATION[0] -> 6_XOut[1:crossfade]
            5_SinOsc[0] -> 6_XOut[2:source]
        }
        ''', str(factory.build()))

    def test_gate_04(self):
        def signal_block(builder, source, state):
            return ugentools.SinOsc.ar()

        factory = synthdeftools.SynthDefFactory(channel_count=1)
        factory.with_signal_block(signal_block)
        factory.with_gate()
        factory.with_output(crossfaded=True, leveled=True, windowed=True)
        self.compare_strings('''
        SynthDef 978267ac37f4bc6993bb7efd71fe8333 {
            0_Control[1] -> 1_Linen[0:gate]
            const_0:0.02 -> 1_Linen[1:attack_time]
            const_1:1.0 -> 1_Linen[2:sustain_level]
            const_0:0.02 -> 1_Linen[3:release_time]
            const_2:2.0 -> 1_Linen[4:done_action]
            const_3:0.0 -> 2_Line[0:start]
            const_1:1.0 -> 2_Line[1:stop]
            0_Control[0] -> 2_Line[2:duration]
            const_2:2.0 -> 2_Line[3:done_action]
            2_Line[0] -> 3_UnaryOpUGen:HANNING_WINDOW[0:source]
            3_UnaryOpUGen:HANNING_WINDOW[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            1_Linen[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            const_4:440.0 -> 5_SinOsc[0:frequency]
            const_3:0.0 -> 5_SinOsc[1:phase]
            5_SinOsc[0] -> 6_BinaryOpUGen:MULTIPLICATION[0:left]
            0_Control[2] -> 6_BinaryOpUGen:MULTIPLICATION[1:right]
            0_Control[3] -> 7_XOut[0:bus]
            4_BinaryOpUGen:MULTIPLICATION[0] -> 7_XOut[1:crossfade]
            6_BinaryOpUGen:MULTIPLICATION[0] -> 7_XOut[2:source]
        }
        ''', str(factory.build()))
