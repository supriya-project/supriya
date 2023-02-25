from ...synthdefs import SynthDefBuilder
from ...ugens import Out, SinOsc


def _build_synthdef():
    with SynthDefBuilder(amplitude=0, bus=0, frequency=440) as builder:
        Out.ar(
            bus=builder["bus"],
            source=SinOsc.ar(frequency=builder["frequency"]) * builder["amplitude"],
        )
    return builder.build(name="simple_sine")


simple_sine = _build_synthdef()


__all__ = ["simple_sine"]
