from ...enums import ParameterRate
from ...ugens import Out, Parameter, SinOsc, SynthDef, SynthDefBuilder


def _build_test_synthdef() -> SynthDef:
    with SynthDefBuilder(
        frequency=440,
        amplitude=Parameter(value=1.0, rate=ParameterRate.AUDIO),
    ) as builder:
        sin_osc = SinOsc.ar(frequency=builder["frequency"])
        enveloped_sin = sin_osc * builder["amplitude"]
        Out.ar(bus=0, source=enveloped_sin)
    return builder.build(name="test")


def _build_test_two_voice_synthdef() -> SynthDef:
    with SynthDefBuilder(
        frequencies=(220, 440),
        amplitude=Parameter(value=1.0, rate=ParameterRate.AUDIO),
    ) as builder:
        sin_osc = SinOsc.ar(frequency=builder["frequencies"])
        enveloped_sin = sin_osc * builder["amplitude"]
        Out.ar(bus=0, source=enveloped_sin)
    return builder.build(name="test_two_voice")


test = _build_test_synthdef()
test_two_voice = _build_test_two_voice_synthdef()

__all__ = ["test", "test_two_voice"]
