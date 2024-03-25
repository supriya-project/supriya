from ...ugens import (
    BPF,
    HPF,
    EnvGen,
    Envelope,
    Out,
    SynthDef,
    SynthDefBuilder,
    WhiteNoise,
)


def _build_clap_synthdef() -> SynthDef:
    with SynthDefBuilder(out=0, amplitude=0.5) as builder:
        envelope_generator_one = EnvGen.ar(
            envelope=Envelope(
                amplitudes=(0, 1, 0, 1, 0, 1, 0, 1, 0),
                durations=(0.001, 0.013, 0, 0.01, 0, 0.01, 0, 0.03),
                curves=(0, -3, 0, -3, 0, -3, 0, -4),
            ),
        )
        envelope_generator_two = EnvGen.ar(
            envelope=Envelope(
                amplitudes=(0, 1, 0), durations=(0.02, 0.3), curves=(0, -4)
            ),
            done_action=2,
        )
        noise_one = (
            BPF.ar(
                source=HPF.ar(
                    source=WhiteNoise.ar(),
                    frequency=600,
                ),
                frequency=2000,
                reciprocal_of_q=3,
            )
            * envelope_generator_one
        )
        noise_two = (
            BPF.ar(
                source=HPF.ar(
                    source=WhiteNoise.ar(),
                    frequency=1000,
                ),
                frequency=1200,
                reciprocal_of_q=0.7,
            )
            * envelope_generator_two
            * 0.7
        )
        Out.ar(
            bus=builder["out"],
            source=[((noise_one + noise_two) * 2).softclip() * builder["amplitude"]]
            * 2,
        )
    return builder.build(name="clap")


clap = _build_clap_synthdef()

__all__ = ["clap"]
