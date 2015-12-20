# -*- encoding: utf-8 -*-
import os
from supriya.tools import nrttools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def test_01():
    session = nrttools.Session()
    builder = synthdeftools.SynthDefBuilder()
    with builder:
        ugentools.Out.ar(bus=0, source=ugentools.SinOsc.ar())
    synthdef = builder.build()
    synth_one = nrttools.Synth(synthdef, 0, 10)
    session.insert([synth_one])
    output_filename = os.path.join(
        os.path.dirname(__file__),
        'output.aiff',
        )
    session.render(output_filename)
