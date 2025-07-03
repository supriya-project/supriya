from uqbar.strings import normalize

from supriya.ugens import SinOsc
from supriya.ugens.factories import SynthDefFactory


def test_gate_01() -> None:
    def signal_block(builder, source, state):
        return SinOsc.ar()

    factory = SynthDefFactory(channel_count=1)
    factory = factory.with_signal_block(signal_block)
    factory = factory.with_gate()
    factory = factory.with_output()
    assert str(factory.build(name="test")) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.ir:
                    out: 0.0
            -   Control.kr:
                    gate: 1.0
            -   Linen.kr:
                    gate: Control.kr[0:gate]
                    attack_time: 0.02
                    sustain_level: 1.0
                    release_time: 0.02
                    done_action: 2.0
            -   SinOsc.ar:
                    frequency: 440.0
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: SinOsc.ar[0]
                    right: Linen.kr[0]
            -   Out.ar:
                    bus: Control.ir[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """
    )


def test_gate_02() -> None:
    def signal_block(builder, source, state):
        return SinOsc.ar()

    factory = SynthDefFactory(channel_count=1)
    factory = factory.with_signal_block(signal_block)
    factory = factory.with_gate()
    factory = factory.with_output(crossfaded=True)
    assert str(factory.build(name="test")) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.ir:
                    out: 0.0
            -   Control.kr:
                    gate: 1.0
                    mix: 0.0
            -   Linen.kr:
                    gate: Control.kr[0:gate]
                    attack_time: 0.02
                    sustain_level: 1.0
                    release_time: 0.02
                    done_action: 2.0
            -   BinaryOpUGen(MULTIPLICATION).kr:
                    left: Control.kr[1:mix]
                    right: Linen.kr[0]
            -   SinOsc.ar:
                    frequency: 440.0
                    phase: 0.0
            -   XOut.ar:
                    bus: Control.ir[0:out]
                    crossfade: BinaryOpUGen(MULTIPLICATION).kr[0]
                    source[0]: SinOsc.ar[0]
        """
    )


def test_gate_03() -> None:
    def signal_block(builder, source, state):
        return SinOsc.ar()

    factory = SynthDefFactory(channel_count=1)
    factory = factory.with_signal_block(signal_block)
    factory = factory.with_gate()
    factory = factory.with_output(crossfaded=True, windowed=True)
    assert str(factory.build(name="test")) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.ir:
                    duration: 1.0
                    out: 0.0
            -   Line.kr:
                    start: 0.0
                    stop: 1.0
                    duration: Control.ir[0:duration]
                    done_action: 2.0
            -   UnaryOpUGen(HANNING_WINDOW).kr:
                    source: Line.kr[0]
            -   Control.kr:
                    gate: 1.0
            -   Linen.kr:
                    gate: Control.kr[0:gate]
                    attack_time: 0.02
                    sustain_level: 1.0
                    release_time: 0.02
                    done_action: 2.0
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
        """
    )


def test_gate_04() -> None:
    def signal_block(builder, source, state):
        return SinOsc.ar()

    factory = SynthDefFactory(channel_count=1)
    factory = factory.with_signal_block(signal_block)
    factory = factory.with_gate()
    factory = factory.with_output(crossfaded=True, leveled=True, windowed=True)
    assert str(factory.build(name="test")) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.ir:
                    duration: 1.0
                    out: 0.0
            -   Line.kr:
                    start: 0.0
                    stop: 1.0
                    duration: Control.ir[0:duration]
                    done_action: 2.0
            -   UnaryOpUGen(HANNING_WINDOW).kr:
                    source: Line.kr[0]
            -   Control.kr:
                    gate: 1.0
                    level: 1.0
            -   Linen.kr:
                    gate: Control.kr[0:gate]
                    attack_time: 0.02
                    sustain_level: 1.0
                    release_time: 0.02
                    done_action: 2.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: UnaryOpUGen(HANNING_WINDOW).kr[0]
                    right: Control.kr[1:level]
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
        """
    )
