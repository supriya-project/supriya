# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya import synthdefs
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

    group_one = [
        patterntools.Pbind(
            duration=1,
            frequency=patterntools.Pseq([1111, 1112, 1113, 1114], 1),
            ),
        patterntools.Pbind(
            duration=1,
            frequency=patterntools.Pseq([2221, 2222, 2223, 2224], 1),
            ),
        ]

    group_two = [
        patterntools.Pbind(
            duration=1,
            frequency=patterntools.Pseq([3331, 3332, 3333, 3334], 1),
            ),
        patterntools.Pbind(
            duration=1,
            frequency=patterntools.Pseq([4441, 4442, 4443, 4444], 1),
            ),
        ]

    pattern = patterntools.Pgfxpar(
        [group_one, group_two],
        synthdef=limiter_synthdef,
        release_time=0.25,
        )
    pattern = pattern.with_bus(release_time=0.25)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_to_lists(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.inscribe(self.pattern)
        d_recv_commands = self.build_d_recv_commands([
            synthdefs.system_link_audio_2,
            synthdefs.default,
            self.limiter_synthdef,
            ])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/g_new', 1002, 1, 1000],
                ['/s_new', '38bda0aee6d0e2d4af72be83c09d9b77', 1003, 3, 1002,
                    'in_', 16, 'out', 16],
                ['/g_new', 1004, 1, 1000],
                ['/s_new', '38bda0aee6d0e2d4af72be83c09d9b77', 1005, 3, 1004,
                    'in_', 16, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1002,
                    'frequency', 1111, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1007, 0, 1002,
                    'frequency', 2221, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1008, 0, 1004,
                    'frequency', 3331, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1009, 0, 1004,
                    'frequency', 4441, 'out', 16]]],
            [1.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1010, 0, 1002,
                    'frequency', 1112, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1011, 0, 1002,
                    'frequency', 2222, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1012, 0, 1004,
                    'frequency', 3332, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1013, 0, 1004,
                    'frequency', 4442, 'out', 16],
                ['/n_set', 1006, 'gate', 0],
                ['/n_set', 1007, 'gate', 0],
                ['/n_set', 1008, 'gate', 0],
                ['/n_set', 1009, 'gate', 0]]],
            [2.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1014, 0, 1002,
                    'frequency', 1113, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1015, 0, 1002,
                    'frequency', 2223, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1016, 0, 1004,
                    'frequency', 3333, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1017, 0, 1004,
                    'frequency', 4443, 'out', 16],
                ['/n_set', 1010, 'gate', 0],
                ['/n_set', 1011, 'gate', 0],
                ['/n_set', 1012, 'gate', 0],
                ['/n_set', 1013, 'gate', 0]]],
            [3.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1018, 0, 1002,
                    'frequency', 1114, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1019, 0, 1002,
                    'frequency', 2224, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1020, 0, 1004,
                    'frequency', 3334, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1021, 0, 1004,
                    'frequency', 4444, 'out', 16],
                ['/n_set', 1014, 'gate', 0],
                ['/n_set', 1015, 'gate', 0],
                ['/n_set', 1016, 'gate', 0],
                ['/n_set', 1017, 'gate', 0]]],
            [4.0, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1018, 'gate', 0],
                ['/n_set', 1019, 'gate', 0],
                ['/n_set', 1020, 'gate', 0],
                ['/n_set', 1021, 'gate', 0]]],
            [4.25, [
                ['/n_free', 1000, 1002, 1003, 1004, 1005],
                [0]]]]

    def test_to_strings(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.inscribe(self.pattern)
        assert session.to_strings() == self.normalize('''
            0.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1007 default
                            1006 default
                        1003 limiter
                        1004 group
                            1009 default
                            1008 default
                        1005 limiter
                    1001 system_link_audio_2
            1.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1011 default
                            1010 default
                        1003 limiter
                        1004 group
                            1013 default
                            1012 default
                        1005 limiter
                    1001 system_link_audio_2
            2.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1015 default
                            1014 default
                        1003 limiter
                        1004 group
                            1017 default
                            1016 default
                        1005 limiter
                    1001 system_link_audio_2
            3.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                            1019 default
                            1018 default
                        1003 limiter
                        1004 group
                            1021 default
                            1020 default
                        1005 limiter
                    1001 system_link_audio_2
            4.0:
                NODE TREE 0 group
                    1000 group
                        1002 group
                        1003 limiter
                        1004 group
                        1005 limiter
            4.25:
                NODE TREE 0 group
            ''')
