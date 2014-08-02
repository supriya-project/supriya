# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def _build_default_synthdef():

    r'''
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
    '''

    builder = synthdeftools.SynthDefBuilder(
        amplitude=0.1,
        frequency=440,
        gate=1,
        out=synthdeftools.Parameter(
            name='out',
            parameter_rate=synthdeftools.ParameterRate.SCALAR,
            value=0,
            ),
        pan=0,
        )

    var_saw = ugentools.VarSaw.ar(
        frequency=builder['frequency'] + (
            0,
            ugentools.Rand.ir(
                minimum=-0.4,
                maximum=0.,
                ),
            ugentools.Rand.ir(
                minimum=0.,
                maximum=0.4,
                ),
            ),
        width=0.3,
        )
    var_saw *= 0.3

    mix = ugentools.Mix.new(var_saw)

    x_line = ugentools.XLine.kr(
        start=ugentools.Rand.ir(
            minimum=4000,
            maximum=5000,
            ),
        stop=ugentools.Rand.ir(
            minimum=2500,
            maximum=3200,
            ),
        )
                
    low_pass = ugentools.LPF.ar(
        source=mix,
        frequency=x_line,
        )

    linen = ugentools.Linen.kr(
        builder['gate'],
        0.01,
        0.7,
        0.3,
        2,
        )

    pan = ugentools.Pan2.ar(
        source=low_pass * linen,
        position=builder['pan'],
        )

    pan *= builder['amplitude']

    output = ugentools.OffsetOut.ar(
        bus=builder['out'],
        source=pan,
        )

    builder.add_ugen(output)
    synthdef = builder.build()
    return synthdef

default = _build_default_synthdef()

__all__ = (
    'default',
    )