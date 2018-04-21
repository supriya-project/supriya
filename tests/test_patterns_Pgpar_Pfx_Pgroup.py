import pytest
import supriya.assets.synthdefs
import supriya.nonrealtime
import supriya.patterns
import supriya.synthdefs
import supriya.ugens
import uqbar.strings


with supriya.synthdefs.SynthDefBuilder(in_=0, out=0) as builder:
    source = supriya.ugens.In.ar(bus=builder['in_'])
    source = supriya.ugens.Limiter.ar(source=source)
    supriya.ugens.Out.ar(bus=builder['out'], source=source)
limiter_synthdef = builder.build()


pattern_one = supriya.patterns.Ppar([
    supriya.patterns.Pbind(
        duration=1,
        frequency=supriya.patterns.Pseq([1111, 1112, 1113], 1),
        ),
    supriya.patterns.Pbind(
        duration=1,
        frequency=supriya.patterns.Pseq([2221, 2222, 2223], 1),
        ),
    ])
pattern_one = pattern_one.with_group()
pattern_one = pattern_one.with_effect(synthdef=limiter_synthdef)


pattern_two = supriya.patterns.Ppar([
    supriya.patterns.Pbind(
        duration=1,
        frequency=supriya.patterns.Pseq([3331, 3332, 3333], 1),
        ),
    supriya.patterns.Pbind(
        duration=1,
        frequency=supriya.patterns.Pseq([4441, 4442, 4443], 1),
        ),
    ])
pattern_two = pattern_two.with_group()
pattern_two = pattern_two.with_effect(synthdef=limiter_synthdef)


pattern = supriya.patterns.Pgpar([
    pattern_one,
    pattern_two,
    ])
pattern = pattern.with_bus()


def test_nonrealtime():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        final_offset = session.inscribe(pattern)
    d_recv_commands = pytest.helpers.build_d_recv_commands([
        supriya.assets.synthdefs.system_link_audio_2,
        supriya.assets.synthdefs.default,
        limiter_synthdef,
        ])
    assert session.to_lists() == [
        [0.0, [
            *d_recv_commands,
            ['/g_new', 1000, 0, 0],
            ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1001, 3, 1000,
                'fade_time', 0.25, 'in_', 16],
            ['/g_new', 1002, 1, 1000],
            ['/g_new', 1003, 1, 1000],
            ['/s_new', '38bda0aee6d0e2d4af72be83c09d9b77', 1004, 1, 1002,
                'in_', 16, 'out', 16],
            ['/g_new', 1005, 0, 1002],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1005,
                'frequency', 1111, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1007, 0, 1005,
                'frequency', 2221, 'out', 16],
            ['/s_new', '38bda0aee6d0e2d4af72be83c09d9b77', 1008, 1, 1003,
                'in_', 16, 'out', 16],
            ['/g_new', 1009, 0, 1003],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1010, 0, 1009,
                'frequency', 3331, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1011, 0, 1009,
                'frequency', 4441, 'out', 16]]],
        [1.0, [
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1012, 0, 1005,
                'frequency', 1112, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1013, 0, 1005,
                'frequency', 2222, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1014, 0, 1009,
                'frequency', 3332, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1015, 0, 1009,
                'frequency', 4442, 'out', 16],
            ['/n_set', 1006, 'gate', 0],
            ['/n_set', 1007, 'gate', 0],
            ['/n_set', 1010, 'gate', 0],
            ['/n_set', 1011, 'gate', 0]]],
        [2.0, [
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1016, 0, 1005,
                'frequency', 1113, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1017, 0, 1005,
                'frequency', 2223, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1018, 0, 1009,
                'frequency', 3333, 'out', 16],
            ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1019, 0, 1009,
                'frequency', 4443, 'out', 16],
            ['/n_set', 1012, 'gate', 0],
            ['/n_set', 1013, 'gate', 0],
            ['/n_set', 1014, 'gate', 0],
            ['/n_set', 1015, 'gate', 0]]],
        [3.0, [
            ['/n_set', 1001, 'gate', 0],
            ['/n_set', 1016, 'gate', 0],
            ['/n_set', 1017, 'gate', 0],
            ['/n_set', 1018, 'gate', 0],
            ['/n_set', 1019, 'gate', 0]]],
        [3.25, [
            ['/n_free', 1000, 1002, 1003, 1004, 1005, 1008, 1009],
            [0]]]]
    assert final_offset == 3.25


def test_to_strings(self):
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.inscribe(pattern)
    assert session.to_strings(include_controls=True) == uqbar.strings.normalize('''
        0.0:
            NODE TREE 0 group
                1000 group
                    1002 group
                        1005 group
                            1007 default
                                amplitude: 0.1, frequency: 2221.0, gate: 1.0, out: a0, pan: 0.5
                            1006 default
                                amplitude: 0.1, frequency: 1111.0, gate: 1.0, out: a0, pan: 0.5
                        1004 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: a0, out: a0
                    1003 group
                        1009 group
                            1011 default
                                amplitude: 0.1, frequency: 4441.0, gate: 1.0, out: a0, pan: 0.5
                            1010 default
                                amplitude: 0.1, frequency: 3331.0, gate: 1.0, out: a0, pan: 0.5
                        1008 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: a0, out: a0
                1001 system_link_audio_2
                    done_action: 2.0, fade_time: 0.25, gate: 1.0, in_: a0, out: 0.0
        1.0:
            NODE TREE 0 group
                1000 group
                    1002 group
                        1005 group
                            1013 default
                                amplitude: 0.1, frequency: 2222.0, gate: 1.0, out: a0, pan: 0.5
                            1012 default
                                amplitude: 0.1, frequency: 1112.0, gate: 1.0, out: a0, pan: 0.5
                        1004 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: 0.0, out: 0.0
                    1003 group
                        1009 group
                            1015 default
                                amplitude: 0.1, frequency: 4442.0, gate: 1.0, out: a0, pan: 0.5
                            1014 default
                                amplitude: 0.1, frequency: 3332.0, gate: 1.0, out: a0, pan: 0.5
                        1008 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: 0.0, out: 0.0
                1001 system_link_audio_2
                    done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        2.0:
            NODE TREE 0 group
                1000 group
                    1002 group
                        1005 group
                            1017 default
                                amplitude: 0.1, frequency: 2223.0, gate: 1.0, out: a0, pan: 0.5
                            1016 default
                                amplitude: 0.1, frequency: 1113.0, gate: 1.0, out: a0, pan: 0.5
                        1004 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: 0.0, out: 0.0
                    1003 group
                        1009 group
                            1019 default
                                amplitude: 0.1, frequency: 4443.0, gate: 1.0, out: a0, pan: 0.5
                            1018 default
                                amplitude: 0.1, frequency: 3333.0, gate: 1.0, out: a0, pan: 0.5
                        1008 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: 0.0, out: 0.0
                1001 system_link_audio_2
                    done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        3.0:
            NODE TREE 0 group
                1000 group
                    1002 group
                        1005 group
                        1004 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: 0.0, out: 0.0
                    1003 group
                        1009 group
                        1008 38bda0aee6d0e2d4af72be83c09d9b77
                            in_: 0.0, out: 0.0
        3.25:
            NODE TREE 0 group
        ''')
