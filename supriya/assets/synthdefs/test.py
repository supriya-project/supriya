import supriya.synthdefs
import supriya.ugens
from supriya import ParameterRate


def _build_test_synthdef():
    with supriya.synthdefs.SynthDefBuilder(
        frequency=440,
        amplitude=supriya.synthdefs.Parameter(
            value=1.0, parameter_rate=ParameterRate.AUDIO
        ),
    ) as builder:
        sin_osc = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        enveloped_sin = sin_osc * builder["amplitude"]
        supriya.ugens.Out.ar(bus=0, source=enveloped_sin)
    synthdef = builder.build(name="test")
    return synthdef


test = _build_test_synthdef()

__all__ = ("test",)
