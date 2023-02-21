import supriya.synthdefs
import supriya.ugens


def _build_clap_synthdef():
    with supriya.synthdefs.SynthDefBuilder(out=0, amplitude=0.5) as builder:
        envelope_one = supriya.synthdefs.Envelope(
            amplitudes=(0, 1, 0, 1, 0, 1, 0, 1, 0),
            durations=(0.001, 0.013, 0, 0.01, 0, 0.01, 0, 0.03),
            curves=(0, -3, 0, -3, 0, -3, 0, -4),
        )
        envelope_generator_one = supriya.ugens.EnvGen.ar(envelope=envelope_one)

        envelope_two = supriya.synthdefs.Envelope(
            amplitudes=(0, 1, 0), durations=(0.02, 0.3), curves=(0, -4)
        )
        envelope_generator_two = supriya.ugens.EnvGen.ar(
            envelope=envelope_two, done_action=2
        )

        noise_one = supriya.ugens.WhiteNoise.ar() * envelope_generator_one
        noise_one = supriya.ugens.HPF.ar(source=noise_one, frequency=600)
        noise_one = supriya.ugens.BPF.ar(
            source=noise_one, frequency=2000, reciprocal_of_q=3
        )

        noise_two = supriya.ugens.WhiteNoise.ar() * envelope_generator_two
        noise_two = supriya.ugens.HPF.ar(source=noise_two, frequency=1000)
        noise_two = supriya.ugens.BPF.ar(
            source=noise_two, frequency=1200, reciprocal_of_q=0.7
        )
        noise_two = noise_two * 0.7

        result = noise_one + noise_two
        result = result * 2
        result = result.softclip()
        result = result * builder["amplitude"]

        supriya.ugens.Out.ar(bus=builder["out"], source=(result, result))

    synthdef = builder.build()
    return synthdef


clap = _build_clap_synthdef()

__all__ = ("clap",)
