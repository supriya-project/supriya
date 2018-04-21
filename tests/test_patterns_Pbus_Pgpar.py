import pytest
import supriya.assets.synthdefs
import supriya.nonrealtime
import supriya.patterns
from patterns_testbase import TestCase


class TestCase(TestCase):

    pattern = supriya.patterns.Pbus(
        supriya.patterns.Pgpar([
            supriya.patterns.Pmono(
                amplitude=1.0,
                duration=1.0,
                frequency=supriya.patterns.Pseq([440, 660, 880, 990], 1),
                ),
            supriya.patterns.Pbind(
                amplitude=1.0,
                duration=0.75,
                frequency=supriya.patterns.Pseq([222, 333, 444, 555], 1),
                ),
            ]),
        )

    def test_manual_incommunicado(self):
        lists, deltas = pytest.helpers.manual_incommunicado(self.pattern, 10)
        assert lists == [
            [10, [
                ['/g_new', 1000, 0, 1],
                ['/s_new', 'system_link_audio_2', 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 0],
                ['/g_new', 1002, 1, 1000],
                ['/g_new', 1003, 1, 1000],
                ['/s_new', 'default', 1004, 0, 1002,
                    'amplitude', 1.0, 'frequency', 440, 'out', 0],
                ['/s_new', 'default', 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 222, 'out', 0]]],
            [10.75, [
                ['/n_set', 1005, 'gate', 0],
                ['/s_new', 'default', 1006, 0, 1003,
                    'amplitude', 1.0, 'frequency', 333, 'out', 0]]],
            [11.0, [['/n_set', 1004, 'amplitude', 1.0, 'frequency', 660, 'out', 0]]],
            [11.5, [
                ['/n_set', 1006, 'gate', 0],
                ['/s_new', 'default', 1007, 0, 1003,
                    'amplitude', 1.0, 'frequency', 444, 'out', 0]]],
            [12.0, [['/n_set', 1004, 'amplitude', 1.0, 'frequency', 880, 'out', 0]]],
            [12.25, [
                ['/n_set', 1007, 'gate', 0],
                ['/s_new', 'default', 1008, 0, 1003,
                    'amplitude', 1.0, 'frequency', 555, 'out', 0]]],
            [13.0, [
                ['/n_set', 1008, 'gate', 0],
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 990, 'out', 0]]],
            [14.0, [
                ['/n_set', 1004, 'gate', 0],
                ['/n_free', 1001]]],
            [14.25, [
                ['/n_free', 1000, 1002, 1003]]]]
        assert deltas == [0.75, 0.25, 0.5, 0.5, 0.25, 0.75, 1.0, 0.25, None]

    def test_nonrealtime(self):
        session = supriya.nonrealtime.Session()
        with session.at(10):
            session.inscribe(self.pattern)
        d_recv_commands = pytest.helpers.build_d_recv_commands([
            supriya.assets.synthdefs.system_link_audio_2,
            supriya.assets.synthdefs.default,
            ])
        assert session.to_lists() == [
            [10.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/g_new', 1002, 1, 1000],
                ['/g_new', 1003, 1, 1000],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1002,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 222, 'out', 16]]],
            [10.75, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1003,
                    'amplitude', 1.0, 'frequency', 333, 'out', 16],
                ['/n_set', 1005, 'gate', 0]]],
            [11.0, [
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 660]]],
            [11.5, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1007, 0, 1003,
                    'amplitude', 1.0, 'frequency', 444, 'out', 16],
                ['/n_set', 1006, 'gate', 0]]],
            [12.0, [
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 880]]],
            [12.25, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1008, 0, 1003,
                    'amplitude', 1.0, 'frequency', 555, 'out', 16],
                ['/n_set', 1007, 'gate', 0]]],
            [13.0, [
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 990],
                ['/n_set', 1008, 'gate', 0]]],
            [14.0, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1004, 'gate', 0]]],
            [14.25, [
                ['/n_free', 1000, 1002, 1003],
                [0]]]]
