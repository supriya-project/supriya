# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pgpar([
        patterntools.Pmono(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([440, 660, 880, 990], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([222, 333, 444, 555], 1),
            ),
        ])

    def test_manual_incommunicado(self):
        lists, deltas = self.manual_incommunicado(self.pattern, 10)
        assert lists == [
            [10, [
                ['/g_new', 1000, 1, 1],
                ['/g_new', 1001, 1, 1],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1001,
                    'amplitude', 1.0, 'frequency', 222]]],
            [10.75, [
                ['/n_set', 1003, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1001,
                    'amplitude', 1.0, 'frequency', 333]]],
            [11.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 660]]],
            [11.5, [
                ['/n_set', 1004, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1001,
                    'amplitude', 1.0, 'frequency', 444]]],
            [12.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 880]]],
            [12.25, [
                ['/n_set', 1005, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1001,
                    'amplitude', 1.0, 'frequency', 555]]],
            [13.0, [
                ['/n_set', 1006, 'gate', 0],
                ['/n_set', 1002, 'amplitude', 1.0, 'frequency', 990]]],
            [14.0, [['/n_set', 1002, 'gate', 0]]],
            [14.25, [['/n_free', 1000, 1001]]]]
        assert deltas == [0.75, 0.25, 0.5, 0.5, 0.25, 0.75, 1.0, 0.25, None]

    def test_nonrealtime(self):
        session = nonrealtimetools.Session()
        with session.at(10):
            self.pattern.inscribe(session)
        assert session.to_lists() == [
            [10.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/g_new', 1000, 1, 0],
                ['/g_new', 1001, 1, 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1001,
                    'amplitude', 1.0, 'frequency', 222]]],
            [10.75, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1001,
                    'amplitude', 1.0, 'frequency', 333],
                ['/n_set', 1003, 'gate', 0]]],
            [11.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 660]]],
            [11.5, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1001,
                    'amplitude', 1.0, 'frequency', 444],
                ['/n_set', 1004, 'gate', 0]]],
            [12.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 880]]],
            [12.25, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1001,
                    'amplitude', 1.0, 'frequency', 555],
                ['/n_set', 1005, 'gate', 0]]],
            [13.0, [
                ['/n_set', 1002, 'amplitude', 1.0, 'frequency', 990],
                ['/n_set', 1006, 'gate', 0]]],
            [14.0, [['/n_set', 1002, 'gate', 0]]],
            [14.25, [['/n_free', 1000, 1001], [0]]]]
