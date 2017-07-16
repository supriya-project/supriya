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
            synthdef:
                name: 937f9dd172e0c2ec52916ce2ae4cb9c1
                ugens:
                -   Control.ir: null
                -   TrigControl.kr: null
                -   Linen.kr:
                        attack_time: 0.02
                        done_action: 2.0
                        gate: TrigControl.kr[0:gate]
                        release_time: 0.02
                        sustain_level: 1.0
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: SinOsc.ar[0]
                        right: Linen.kr[0]
                -   Out.ar:
                        bus: Control.ir[0:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
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
            synthdef:
                name: b2b4641122aa7170a652c245e97f995e
                ugens:
                -   Control.ir: null
                -   TrigControl.kr: null
                -   Linen.kr:
                        attack_time: 0.02
                        done_action: 2.0
                        gate: TrigControl.kr[0:gate]
                        release_time: 0.02
                        sustain_level: 1.0
                -   Control.kr: null
                -   BinaryOpUGen(MULTIPLICATION).kr:
                        left: Control.kr[0:crossfade]
                        right: Linen.kr[0]
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   XOut.ar:
                        bus: Control.ir[0:out]
                        crossfade: BinaryOpUGen(MULTIPLICATION).kr[0]
                        source[0]: SinOsc.ar[0]
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
            synthdef:
                name: 7758ec85f0a5e78d07ac88e6e9ac17db
                ugens:
                -   Control.ir: null
                -   Line.kr:
                        done_action: 2.0
                        duration: Control.ir[0:duration]
                        start: 0.0
                        stop: 1.0
                -   UnaryOpUGen(HANNING_WINDOW).kr:
                        source: Line.kr[0]
                -   TrigControl.kr: null
                -   Linen.kr:
                        attack_time: 0.02
                        done_action: 2.0
                        gate: TrigControl.kr[0:gate]
                        release_time: 0.02
                        sustain_level: 1.0
                -   BinaryOpUGen(MULTIPLICATION).kr:
                        left: UnaryOpUGen(HANNING_WINDOW).kr[0]
                        right: Linen.kr[0]
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   XOut.ar:
                        bus: Control.ir[1:out]
                        crossfade: BinaryOpUGen(MULTIPLICATION).kr[0]
                        source[0]: SinOsc.ar[0]
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
            synthdef:
                name: 976b3fc57d1862cb178148b04472e51c
                ugens:
                -   Control.ir: null
                -   Line.kr:
                        done_action: 2.0
                        duration: Control.ir[0:duration]
                        start: 0.0
                        stop: 1.0
                -   UnaryOpUGen(HANNING_WINDOW).kr:
                        source: Line.kr[0]
                -   TrigControl.kr: null
                -   Linen.kr:
                        attack_time: 0.02
                        done_action: 2.0
                        gate: TrigControl.kr[0:gate]
                        release_time: 0.02
                        sustain_level: 1.0
                -   Control.kr: null
                -   BinaryOpUGen(MULTIPLICATION).kr/0:
                        left: UnaryOpUGen(HANNING_WINDOW).kr[0]
                        right: Control.kr[0:level]
                -   BinaryOpUGen(MULTIPLICATION).kr/1:
                        left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                        right: Linen.kr[0]
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   XOut.ar:
                        bus: Control.ir[1:out]
                        crossfade: BinaryOpUGen(MULTIPLICATION).kr/1[0]
                        source[0]: SinOsc.ar[0]
            ''', str(factory.build()))
