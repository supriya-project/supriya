from ...enums import ParameterRate
from ...synthdefs import Parameter, SynthDefBuilder
from ...ugens import Out, SinOsc


def _build_test_synthdef():
    with SynthDefBuilder(
        frequency=440,
        amplitude=Parameter(value=1.0, parameter_rate=ParameterRate.AUDIO),
    ) as builder:
        sin_osc = SinOsc.ar(frequency=builder["frequency"])
        enveloped_sin = sin_osc * builder["amplitude"]
        Out.ar(bus=0, source=enveloped_sin)
    synthdef = builder.build(name="test")
    return synthdef


test = _build_test_synthdef()

__all__ = ("test",)
