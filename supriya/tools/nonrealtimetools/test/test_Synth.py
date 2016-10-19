# -*- encoding: utf-8 -*-
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from base import TestCase


class TestCase(TestCase):

    def test_01(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(
                duration=4,
                synthdef=synthdefs.default,
                )
        with session.at(2):
            session.add_synth(
                duration=4,
                synthdef=synthdefs.default,
                amplitude=0.5,
                frequency=443,
                pan=0.75,
                out=8,
                )
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 0]]],
            [2.0, [['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 0,
                'amplitude', 0.5,
                'frequency', 443,
                'out', 8,
                'pan', 0.75]]],
            [4.0, [['/n_set', 1000, 'gate', 0]]],
            [6.0, [['/n_set', 1001, 'gate', 0], [0]]]]

    def test_01b(self):
        session = nonrealtimetools.Session()
        with session.at(10):
            synth = session.add_synth(
                duration=6,
                synthdef=synthdefs.default,
                frequency=440,
                )
        with session.at(11):
            synth['frequency'] = 442
        with session.at(13):
            synth['frequency'] = 443
        assert session.to_lists() == [
            [10.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 0, 'frequency', 440]]],
            [11.0, [['/n_set', 1000, 'frequency', 442]]],
            [13.0, [['/n_set', 1000, 'frequency', 443]]],
            [16.0, [['/n_set', 1000, 'gate', 0], [0]]],
            ]

    def test_02(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            synth_one = session.add_synth(
                duration=4,
                synthdef=synthdefs.default,
                )
        with session.at(2):
            synth_two = session.add_synth(
                duration=6,
                synthdef=synthdefs.default,
                frequency=330,
                )
        # make settings
        with session.at(2):
            synth_one['frequency'] = 550
            synth_two['frequency'] = 333
        with session.at(3):
            synth_one['frequency'] = 660
            synth_two['frequency'] = 770
        with session.at(4):
            synth_two['frequency'] = 880
        # check settings
        with session.at(0):
            assert synth_one['frequency'] == 440
        with session.at(1):
            assert synth_one['frequency'] == 440
        with session.at(2):
            assert synth_one['frequency'] == 550
            assert synth_two['frequency'] == 333
        with session.at(3):
            assert synth_one['frequency'] == 660
            assert synth_two['frequency'] == 770
        with session.at(4):
            assert synth_two['frequency'] == 880
        with session.at(5):
            assert synth_two['frequency'] == 880

    def test_03(self):
        r'''Durated synths.'''
        synthdef = self.build_duration_synthdef()
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(duration=2, synthdef=synthdef)
            session.add_synth(duration=4, synthdef=synthdef)
            session.add_synth(duration=6, synthdef=synthdef)
            session.add_synth(synthdef=synthdef)
        with session.at(1):
            session.add_synth(duration=4, synthdef=synthdef)
        assert session.to_lists(duration=3) == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1000, 0, 0, 'duration', 2.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1001, 0, 0, 'duration', 3.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1002, 0, 0, 'duration', 3.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1003, 0, 0, 'duration', 3.0]]],
            [1.0, [
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1004, 0, 0, 'duration', 2.0]]],
            [2.0, [['/n_free', 1000]]],
            [3.0, [['/n_free', 1001, 1002, 1003, 1004], [0]]]
            ]
        assert session.to_lists(duration=4) == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1000, 0, 0, 'duration', 2.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1001, 0, 0, 'duration', 4.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1002, 0, 0, 'duration', 4.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1003, 0, 0, 'duration', 4.0]]],
            [1.0,
                [['/s_new', '448a8d487adfc99ec697033edc2a1227', 1004, 0, 0, 'duration', 3.0]]],
            [2.0, [['/n_free', 1000]]],
            [4.0, [['/n_free', 1001, 1002, 1003, 1004], [0]]]
            ]
        assert session.to_lists(duration=5) == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1000, 0, 0, 'duration', 2.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1001, 0, 0, 'duration', 4.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1002, 0, 0, 'duration', 5.0],
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1003, 0, 0, 'duration', 5.0]]],
            [1.0, [
                ['/s_new', '448a8d487adfc99ec697033edc2a1227', 1004, 0, 0, 'duration', 4.0]]],
            [2.0, [['/n_free', 1000]]],
            [4.0, [['/n_free', 1001]]],
            [5.0, [['/n_free', 1002, 1003, 1004], [0]]]
            ]

    def test_04(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            group_a = session.add_group()
            group_b = group_a.add_group()
            synth_a = group_a.add_synth(synthdef=synthdefs.default)
            synth_b = group_b.add_synth(synthdef=synthdefs.default)
        with session.at(2):
            group_a['frequency'] = 440
            group_b['frequency'] = 441
            synth_a['frequency'] = 442
            synth_b['frequency'] = 443
        with session.at(4):
            group_b.move_node(synth_a)
            group_a['frequency'] = 444
            group_b['frequency'] = 445
            synth_a['frequency'] = 446
            synth_b['frequency'] = 447
        assert session.to_lists(duration=6) == [
            [0.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/g_new', 1000, 0, 0],
                ['/g_new', 1001, 0, 1000],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1001]]],
            [2.0, [
                ['/n_set', 1000, 'frequency', 440],
                ['/n_set', 1002, 'frequency', 442],
                ['/n_set', 1001, 'frequency', 441],
                ['/n_set', 1003, 'frequency', 443]]],
            [4.0, [
                ['/g_head', 1001, 1002],
                ['/n_set', 1000, 'frequency', 444],
                ['/n_set', 1001, 'frequency', 445],
                ['/n_set', 1002, 'frequency', 446],
                ['/n_set', 1003, 'frequency', 447]]],
            [6.0, [
                ['/n_free', 1000, 1001],
                ['/n_set', 1002, 'gate', 0],
                ['/n_set', 1003, 'gate', 0],
                [0]]],
            ]

    def test_05(self):
        session = nonrealtimetools.Session()
        synthdef = self.build_basic_synthdef()
        with session.at(0):
            session.add_synth(
                duration=0,
                synthdef=synthdef,
                )
        assert session.to_lists(duration=1) == [
            [0.0, [
                ['/d_recv', bytearray(synthdef.compile())],
                ['/s_new', 'd719856d7deff2696a3f807f5dc79809', 1000, 0, 0]]],
            [1.0, [[0]]]
            ]
