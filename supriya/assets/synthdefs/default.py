from ...enums import DoneAction, ParameterRate
from ...ugens import (
    LPF,
    Linen,
    Mix,
    OffsetOut,
    Pan2,
    Parameter,
    Rand,
    SynthDef,
    SynthDefBuilder,
    VarSaw,
    XLine,
)


def _build_default_synthdef() -> SynthDef:
    with SynthDefBuilder(
        amplitude=0.1,
        frequency=440,
        gate=1,
        out=Parameter(rate=ParameterRate.SCALAR, value=0),
        pan=0.5,
    ) as builder:
        low_pass = LPF.ar(
            source=Mix.new(
                VarSaw.ar(
                    frequency=builder["frequency"]
                    + (
                        0,
                        Rand.ir(minimum=-0.4, maximum=0.0),
                        Rand.ir(minimum=0.0, maximum=0.4),
                    ),
                    width=0.3,
                )
            )
            * 0.3,
            frequency=XLine.kr(
                start=Rand.ir(minimum=4000, maximum=5000),
                stop=Rand.ir(minimum=2500, maximum=3200),
            ),
        )
        linen = Linen.kr(
            attack_time=0.01,
            done_action=DoneAction.FREE_SYNTH,
            gate=builder["gate"],
            release_time=0.3,
            sustain_level=0.7,
        )
        pan = Pan2.ar(
            source=low_pass * linen * builder["amplitude"], position=builder["pan"]
        )
        OffsetOut.ar(bus=builder["out"], source=pan)
    return builder.build(name="supriya:default")


default = _build_default_synthdef()

__all__ = ["default"]
