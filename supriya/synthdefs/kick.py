# =*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def _build_kick_synthdef():

    builder = synthdeftools.SynthDefBuilder(
        out=0,
        )

    with builder:

        ### ENVELOPE ###

        gate = ugentools.Impulse.ar(frequency=2)
        envelope = synthdeftools.Envelope.percussive(
            attack_time=0.01,
            release_time=1.0,
            )
        envelope = ugentools.EnvGen.ar(
            done_action=0,
            envelope=envelope,
            gate=gate
            )
        envelope = envelope.squared()

        ### NOISE COMPONENT ###

        noise = ugentools.PinkNoise.ar()
        noise = ugentools.BPF.ar(
            source=noise,
            frequency=ugentools.LinLin.ar(
                source=envelope.cubed(),
                output_minimum=30,
                output_maximum=120,
                ),
            reciprocal_of_q=2,
            )
        noise *= envelope

        ### PITCHED COMPONENT ###

        pitch = ugentools.SinOsc.ar(
            frequency=ugentools.LinLin.ar(
                source=envelope,
                output_minimum=10,
                output_maximum=80,
                ),
            )
        pitch = pitch * 2.0
        pitch = pitch.distort()
        pitch = ugentools.RLPF.ar(
            source=pitch,
            frequency=ugentools.LinLin.ar(
                source=envelope,
                output_minimum=30,
                output_maximum=120,
                ),
            reciprocal_of_q=0.5,
            )
        pitch *= envelope

        mix = pitch + noise

        ugentools.Out.ar(builder['out'], (mix, mix))

    synthdef = builder.build()
    return synthdef

kick = _build_kick_synthdef()

__all__ = (
    'kick',
    )
