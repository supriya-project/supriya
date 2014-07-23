# =*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def _build_kick_synthdef():

    builder = synthdeftools.SynthDefBuilder(
        out=0,
        )

    envelope = synthdeftools.Envelope.percussive(
        attack_time=0.0001,
        release_time=0.4,
        )
    envelope = ugentools.EnvGen.ar(
        envelope=envelope,
        done_action=2,
        )
    envelope = synthdeftools.Op.squared(envelope)

    noise = ugentools.WhiteNoise.ar()
    noise = ugentools.RLPF.ar(
        source=noise,
        frequency=ugentools.LinLin.ar(
            source=synthdeftools.Op.squared(envelope),
            out_min=40,
            out_max=220,
            ),
        reciprocal_of_q=10,
        )
    noise = ugentools.HPF.ar(
        source=noise,
        frequency=200,
        )
    noise = noise * envelope * 40
    noise = synthdeftools.Op.tanh(noise)

    saw_a = ugentools.LFSaw.ar(frequency=40)
    saw_a = ugentools.RLPF.ar(
        source=saw_a,
        frequency=ugentools.LinLin.ar(
            source=synthdeftools.Op.squared(envelope),
            out_min=30,
            out_max=120,
            ),
        reciprocal_of_q=0.001,
        )
    saw_a = saw_a * envelope * 0.1
    saw_a = synthdeftools.Op.tanh(saw_a)

    saw_b = ugentools.LFSaw.ar(frequency=39)
    saw_b = ugentools.RLPF.ar(
        source=saw_b,
        frequency=ugentools.LinLin.ar(
            source=synthdeftools.Op.squared(envelope),
            out_min=20,
            out_max=150,
            ),
        reciprocal_of_q=0.001,
        )
    saw_b = saw_b * envelope * 0.1
    saw_b = synthdeftools.Op.tanh(saw_b)

    mix = 0
    mix += noise * 0.05
    mix += saw_a
    mix += saw_b
    mix *= 2.0
    mix = ugentools.CompanderD.ar(
        source=mix,
        relax_time=0.1,
        slope_below=0.5,
        thresh=0.3,
        )

    out = ugentools.Out.ar(builder['out'], (mix, mix))

    builder.add_ugen(out)
    synthdef = builder.build()
    return synthdef

kick = _build_kick_synthdef()

__all__ = (
    'kick',
    )