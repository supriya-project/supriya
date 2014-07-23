# =*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools

r'''
(
{
    var envelope, noise, saw_a, saw_b, mix;

    envelope = EnvGen.ar(Env.perc(0.0001, 0.5), doneAction: 2).squared;

    noise = RLPF.ar(
        in: WhiteNoise.ar,
        freq: LinLin.ar(in: envelope.squared, dstlo: 0, dsthi: 150),
        rq: 10,
    );
    noise = HPF.ar(
        in: noise,
        freq: 200,
    );
    noise = noise * envelope * 40;
    noise = noise.tanh;
    noise = noise * 0.1;

    saw_a = RLPF.ar(
        in: LFSaw.ar(freq: 59),
        freq: LinLin.ar(in: envelope, dstlo: 30, dsthi: 120),
        rq: 0.001,
    );
    saw_a = saw_a * envelope * 0.2;
    saw_a = saw_a.tanh;

    saw_b = RLPF.ar(
        in: LFSaw.ar(freq: 60),
        freq: LinLin.ar(in: envelope, dstlo: 0, dsthi: 80),
        rq: 0.001,
    );
    saw_b = saw_b * envelope * 0.1;
    saw_b = saw_b.tanh;

    mix = 0;
    mix = mix + noise;
    mix = mix + saw_a;
    mix = mix + saw_b;
    Out.ar(0, [mix, mix])

}.play
)
'''

def _build_kick_synthdef():

    builder = synthdeftools.SynthDefBuilder(
        out=0,
        )

    envelope = synthdeftools.Envelope.percussive(
        attack_time=0.0001,
        release_time=0.5,
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
            out_low=0,
            out_high=150,
            ),
        reciprocal_q=10,
        )
    noise = ugentools.HPF.ar(
        source=noise,
        frequency=200,
        )
    noise = noise * envelope * 40
    noise = synthdeftools.Op.tanh(noise)
    noise = noise * 0.1

    saw_a = ugentools.LFSaw.ar(frequency=59)
    saw_a = ugentools.RLPF.ar(
        source=saw_a,
        frequency=ugentools.LinLin.ar(
            source=synthdeftools.Op.squared(envelope),
            out_low=30,
            out_high=120,
            ),
        reciprocal_q=0.001,
        )
    saw_a = saw_a * envelope * 0.1
    saw_a = synthdeftools.Op.tanh(saw_a)

    saw_b = ugentools.LFSaw.ar(frequency=60)
    saw_b = ugentools.RLPF.ar(
        source=saw_b,
        frequency=ugentools.LinLin.ar(
            source=synthdeftools.Op.squared(envelope),
            out_low=30,
            out_high=120,
            ),
        reciprocal_q=0.001,
        )
    saw_b = saw_b * envelope * 0.1
    saw_b = synthdeftools.Op.tanh(saw_b)

    mix = noise + saw_a + saw_b

    out = ugentools.Out.ar(builder['out'], (mix, mix))

    builder.add_ugen(out)
    synthdef = builder.build()
    return synthdef

kick = _build_kick_synthdef()

__all__ = (
    'kick',
    )