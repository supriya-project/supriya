# -*- encoding: utf-8 -*-
import os
from supriya.tools import nrttools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


output_filepath = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    'output.aiff',
    ))


def test_01():
    session = nrttools.Session()
    builder = synthdeftools.SynthDefBuilder()
    with builder:
        ugentools.Out.ar(bus=0, source=ugentools.SinOsc.ar())
    synthdef = builder.build()
    synth_one = nrttools.Synth(synthdef, 0, 10)
    session.insert([synth_one])
    exit_code, _ = session.render(output_filepath)
    output_file_exists = os.path.exists(output_filepath)
    if output_file_exists:
        os.remove(output_filepath)
    assert output_file_exists
    assert exit_code == 0
