# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def _build_test_synthdef():
    builder = synthdeftools.SynthDefBuilder()
    builder.add_parameter('frequency', 440)
    builder.add_parameter('amplitude', 1.0, 'audio')
    with builder:
        sin_osc = ugentools.SinOsc.ar(frequency=builder['frequency'])
        enveloped_sin = sin_osc * builder['amplitude']
        ugentools.Out.ar(bus=0, source=enveloped_sin)
    synthdef = builder.build(name='test')
    return synthdef

test = _build_test_synthdef()

__all__ = (
    'test',
    )
