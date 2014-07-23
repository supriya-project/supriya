# =*- encoding: utf-8 -*-

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