import supriya


def _build_synthdef():
    with supriya.SynthDefBuilder(amplitude=0, bus=0, frequency=440) as builder:
        supriya.ugens.Out.ar(
            bus=builder["bus"],
            source=supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
            * builder["amplitude"],
        )
    return builder.build(name="simple_sine")


simple_sine = _build_synthdef()


__all__ = ["simple_sine"]
