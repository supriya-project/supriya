# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya import AddAction
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(TestCase):

    with synthdeftools.SynthDefBuilder(in_=0, out=0) as builder:
        source = ugentools.In.ar(bus=builder['in_'])
        source = ugentools.Limiter.ar(source=source)
        ugentools.Out.ar(bus=builder['out'], source=source)
    limiter_synthdef = builder.build(name='limiter')

    with synthdeftools.SynthDefBuilder(out=0, duration=1) as builder:
        line = ugentools.Line.kr(duration=builder['duration'], done_action=2)
        source = ugentools.SinOsc.ar() * line.hanning_window()
        ugentools.Out.ar(bus=builder['out'], source=source)
    sine_synthdef = builder.build(name='sine')

    with synthdeftools.SynthDefBuilder(out=0, duration=1) as builder:
        line = ugentools.Line.kr(duration=builder['duration'], done_action=2)
        source = ugentools.PinkNoise.ar() * line.hanning_window()
        ugentools.Out.ar(bus=builder['out'], source=source)
    pink_synthdef = builder.build(name='pink')

    release_time = 9
    pattern = patterntools.Ppar([
        patterntools.Pbind(
            synthdef=sine_synthdef,
            add_action=AddAction.ADD_TO_HEAD,
            duration=40,
            delta=15,
            ),
        patterntools.Pbind(
            synthdef=pink_synthdef,
            add_action=AddAction.ADD_TO_HEAD,
            duration=32,
            delta=16,
            ),
        ])
    pattern = pattern.with_group(release_time=release_time)
    pattern = pattern.with_effect(limiter_synthdef, release_time=release_time)
    pattern = patterntools.Pgpar([pattern], release_time=release_time)
    pattern = pattern.with_bus(release_time=release_time, channel_count=1)

    def test_01(self):
        session = nonrealtimetools.Session(0, 1)
        with session.at(0):
            session.inscribe(self.pattern, duration=60)
        assert session.to_strings() == self.normalize('''
        ''')
        assert session.to_lists() == []
