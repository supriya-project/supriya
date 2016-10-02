# -*- encoding: utf-8 -*-
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from base import TestCase


class TestCase(TestCase):

    def test_01(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_group(duration=20)
            group_b = session.add_group(duration=20)
            group_b.add_synth(duration=20)
        assert session.to_strings(True) == self.normalize('''
            0.0:
                NODE TREE 0 group
                    1001 group
                        1002 da0982184cc8fa54cf9d288a0fe1f6ca
                            amplitude: 0.1, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
                    1000 group
            20.0:
                NODE TREE 0 group
            ''')
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/g_new', 1000, 0, 0],
                ['/g_new', 1001, 0, 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1001]]],
            [20.0, [
                ['/n_free', 1000, 1001],
                ['/n_set', 1002, 'gate', 0],
                [0]]]]
        session.rebuild_transitions()
        assert session.to_strings(True) == self.normalize('''
            0.0:
                NODE TREE 0 group
                    1001 group
                        1002 da0982184cc8fa54cf9d288a0fe1f6ca
                            amplitude: 0.1, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
                    1000 group
            20.0:
                NODE TREE 0 group
            ''')
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/g_new', 1001, 0, 0],
                ['/g_new', 1000, 3, 1001],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1001]]],
            [20.0, [
                ['/n_free', 1000, 1001],
                ['/n_set', 1002, 'gate', 0],
                [0]]]]
