import supriya.synthdefs
import supriya.ugens


def _build_default_synthdef():
    r"""
    SynthDef(\default, { arg out=0, freq=440, amp=0.1, pan=0, gate=1;
        var z;
        z = LPF.ar(
            Mix.new(
                VarSaw.ar(
                    freq + [0, Rand(-0.4, 0.0), Rand(0.0, 0.4)],
                    0,
                    0.3,
                    0.3
                    )
                ),
            XLine.kr(Rand(4000,5000), Rand(2500,3200), 1)
            );
        z = z * Linen.kr(gate, 0.01, 0.7, 0.3, 2);
        OffsetOut.ar(out, Pan2.ar(z, pan, amp));
    }, [\ir]).add;
    """

    builder = supriya.synthdefs.SynthDefBuilder(
        amplitude=0.1,
        frequency=440,
        gate=1,
        out=supriya.synthdefs.Parameter(
            parameter_rate=supriya.ParameterRate.SCALAR, value=0
        ),
        pan=0.5,
    )

    with builder:
        low_pass = supriya.ugens.LPF.ar(
            source=supriya.ugens.Mix.new(
                supriya.ugens.VarSaw.ar(
                    frequency=builder["frequency"]
                    + (
                        0,
                        supriya.ugens.Rand.ir(minimum=-0.4, maximum=0.0),
                        supriya.ugens.Rand.ir(minimum=0.0, maximum=0.4),
                    ),
                    width=0.3,
                )
            )
            * 0.3,
            frequency=supriya.ugens.XLine.kr(
                start=supriya.ugens.Rand.ir(minimum=4000, maximum=5000),
                stop=supriya.ugens.Rand.ir(minimum=2500, maximum=3200),
            ),
        )
        linen = supriya.ugens.Linen.kr(
            attack_time=0.01,
            done_action=supriya.DoneAction.FREE_SYNTH,
            gate=builder["gate"],
            release_time=0.3,
            sustain_level=0.7,
        )
        pan = supriya.ugens.Pan2.ar(
            source=low_pass * linen * builder["amplitude"], position=builder["pan"]
        )
        supriya.ugens.OffsetOut.ar(bus=builder["out"], source=pan)
    synthdef = builder.build(name="default")
    return synthdef


default = _build_default_synthdef()

__all__ = ["default"]
