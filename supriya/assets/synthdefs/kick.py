from supriya.ugens import (
    BPF,
    RLPF,
    EnvGen,
    Envelope,
    Impulse,
    LinLin,
    Out,
    PinkNoise,
    SinOsc,
    SynthDef,
    SynthDefBuilder,
)


def _build_kick_synthdef() -> SynthDef:
    with SynthDefBuilder(out=0) as builder:
        gate = Impulse.ar(frequency=2)
        envelope = EnvGen.ar(
            done_action=0,
            envelope=Envelope.percussive(attack_time=0.01, release_time=1.0),
            gate=gate,
        ).squared()
        noise = BPF.ar(
            source=PinkNoise.ar(),
            frequency=LinLin.ar(
                source=envelope.cubed(), output_minimum=30, output_maximum=120
            ),
            reciprocal_of_q=2,
        )
        pitch = RLPF.ar(
            source=(
                SinOsc.ar(
                    frequency=LinLin.ar(
                        source=envelope, output_minimum=10, output_maximum=80
                    )
                )
                * 2
            ).distort(),
            frequency=LinLin.ar(source=envelope, output_minimum=30, output_maximum=120),
            reciprocal_of_q=0.5,
        )
        mix = (pitch + noise) * envelope
        Out.ar(
            bus=builder["out"],
            source=[mix] * 2,
        )
    return builder.build(name="kick")


kick = _build_kick_synthdef()

__all__ = ["kick"]
