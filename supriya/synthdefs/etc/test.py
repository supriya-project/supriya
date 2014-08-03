# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def _build_test_synthdef():

    builder = synthdeftools.SynthDefBuilder()
    builder.add_ugen(
        ugentools.Out.ar(
            source=ugentools.SinOsc.ar(),
            ),
        )
    synthdef = builder.build(name='test')
    return synthdef

test = _build_test_synthdef()

__all__ = (
    'test',
    )