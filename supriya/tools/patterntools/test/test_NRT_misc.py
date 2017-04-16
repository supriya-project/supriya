# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya import AddAction, synthdefs
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
            0.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1004 group
                                1006 pink
                                1005 sine
                            1003 limiter
                    1001 system_link_audio_1
            15.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1004 group
                                1007 sine
                                1006 pink
                                1005 sine
                            1003 limiter
                    1001 system_link_audio_1
            16.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1004 group
                                1008 pink
                                1007 sine
                                1006 pink
                                1005 sine
                            1003 limiter
                    1001 system_link_audio_1
            30.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1004 group
                                1008 pink
                                1007 sine
                                1006 pink
                                1005 sine
                            1003 limiter
            32.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1004 group
                                1008 pink
                                1007 sine
                                1005 sine
                            1003 limiter
            39.0:
                NODE TREE 0 group
                    1005 sine
                    1007 sine
                    1008 pink
            40.0:
                NODE TREE 0 group
                    1007 sine
                    1008 pink
            48.0:
                NODE TREE 0 group
                    1007 sine
            55.0:
                NODE TREE 0 group
            ''')
        d_recv_commands = []
        for synthdef in sorted(
            [
                synthdefs.system_link_audio_1,
                self.sine_synthdef,
                self.pink_synthdef,
                self.limiter_synthdef,
                ],
            key=lambda x: x.anonymous_name,
            ):
            compiled_synthdef = bytearray(synthdef.compile())
            d_recv_commands.append(['/d_recv', compiled_synthdef])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', '2aa2f6c46d902276bad2e942125ef247', 1001, 3, 1000,
                    'fade_time', 9.0, 'in_', 1],
                ['/g_new', 1002, 1, 1000],
                ['/s_new', '38bda0aee6d0e2d4af72be83c09d9b77', 1003, 1, 1002,
                    'in_', 1, 'out', 1],
                ['/g_new', 1004, 0, 1002],
                ['/s_new', '00a1f31c719b7e5a30788b0d2e78a2cd', 1005, 0, 1004,
                    'duration', 40.0, 'out', 1],
                ['/s_new', '48dcd0cdb5ded3e947186fa74f097516', 1006, 0, 1004,
                    'duration', 32.0, 'out', 1]]],
            [15.0, [
                ['/s_new', '00a1f31c719b7e5a30788b0d2e78a2cd', 1007, 0, 1004,
                    'duration', 40.0, 'out', 1]]],
            [16.0, [
                ['/s_new', '48dcd0cdb5ded3e947186fa74f097516', 1008, 0, 1004,
                    'duration', 32.0, 'out', 1]]],
            [30.0, [['/n_set', 1001, 'gate', 0]]],
            [32.0, [['/n_free', 1006]]],
            [39.0, [
                ['/g_head', 0, 1005],
                ['/n_after', 1007, 1005],
                ['/n_after', 1008, 1007],
                ['/n_free', 1000, 1002, 1003, 1004]]],
            [40.0, [['/n_free', 1005]]],
            [48.0, [['/n_free', 1008]]],
            [55.0, [['/n_free', 1007], [0]]]]
