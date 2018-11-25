import supriya.synthdefs
import supriya.ugens


def _build_kick_synthdef():

    builder = supriya.synthdefs.SynthDefBuilder(out=0)

    with builder:

        ### ENVELOPE ###

        gate = supriya.ugens.Impulse.ar(frequency=2)
        envelope = supriya.synthdefs.Envelope.percussive(
            attack_time=0.01, release_time=1.0
        )
        envelope = supriya.ugens.EnvGen.ar(done_action=0, envelope=envelope, gate=gate)
        envelope = envelope.squared()

        ### NOISE COMPONENT ###

        noise = supriya.ugens.PinkNoise.ar()
        noise = supriya.ugens.BPF.ar(
            source=noise,
            frequency=supriya.ugens.LinLin.ar(
                source=envelope.cubed(), output_minimum=30, output_maximum=120
            ),
            reciprocal_of_q=2,
        )
        noise *= envelope

        ### PITCHED COMPONENT ###

        pitch = supriya.ugens.SinOsc.ar(
            frequency=supriya.ugens.LinLin.ar(
                source=envelope, output_minimum=10, output_maximum=80
            )
        )
        pitch = pitch * 2.0
        pitch = pitch.distort()
        pitch = supriya.ugens.RLPF.ar(
            source=pitch,
            frequency=supriya.ugens.LinLin.ar(
                source=envelope, output_minimum=30, output_maximum=120
            ),
            reciprocal_of_q=0.5,
        )
        pitch *= envelope

        mix = pitch + noise

        supriya.ugens.Out.ar(builder["out"], (mix, mix))

    synthdef = builder.build()
    return synthdef


kick = _build_kick_synthdef()

__all__ = ("kick",)
