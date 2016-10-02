# -*- encoding: utf-8 -*-
import types
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools
from supriya.tools import servertools
from supriya.tools import synthdeftools


class TestCase(systemtools.TestCase):

    pattern = patterntools.Pbus(
        patterntools.Pgpar([
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
            ]),
        )

    def setUp(self):
        self.server = servertools.Server.get_default_server().boot()
        synthdefs.default.allocate(self.server)
        self.server.sync()

    def tearDown(self):
        self.server.quit()

    def manual_incommunicado(self, pattern, timestamp=10):
        player = patterntools.RealtimeEventPlayer(
            pattern,
            server=types.SimpleNamespace(
                audio_bus_allocator=servertools.BlockAllocator(),
                control_bus_allocator=servertools.BlockAllocator(),
                node_id_allocator=servertools.NodeIdAllocator(),
                ),
            )
        lists, deltas, delta = [], [], True
        while delta is not None:
            bundle, delta = player(timestamp, timestamp, communicate=False)
            if delta is not None:
                timestamp += delta
            lists.append(bundle.to_list(True))
            deltas.append(delta)
        return lists, deltas

    def test_manual_incommunicado(self):
        lists, deltas = self.manual_incommunicado(self.pattern, 10)
        assert lists == [
            [10, [
                ['/g_new', 1000, 0, 1],
                ['/s_new', '454b69a7c505ddecc5b39762d291a5ec', 1001, 3, 1000,
                    'in_', 0],
                ['/g_new', 1002, 1, 1000],
                ['/g_new', 1003, 1, 1000],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1002,
                    'amplitude', 1.0, 'frequency', 440, 'out', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 222, 'out', 0]]],
            [10.75, [
                ['/n_set', 1005, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1003,
                    'amplitude', 1.0, 'frequency', 333, 'out', 0]]],
            [11.0, [['/n_set', 1004, 'amplitude', 1.0, 'frequency', 660, 'out', 0]]],
            [11.5, [
                ['/n_set', 1006, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1007, 0, 1003,
                    'amplitude', 1.0, 'frequency', 444, 'out', 0]]],
            [12.0, [['/n_set', 1004, 'amplitude', 1.0, 'frequency', 880, 'out', 0]]],
            [12.25, [
                ['/n_set', 1007, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1008, 0, 1003,
                    'amplitude', 1.0, 'frequency', 555, 'out', 0]]],
            [13.0, [
                ['/n_set', 1008, 'gate', 0],
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 990, 'out', 0]]],
            [14.0, [['/n_set', 1004, 'gate', 0]]],
            [14.25, [['/n_free', 1002, 1003]]],
            [14.5, [['/n_free', 1000, 1001]]]]
        assert deltas == [0.75, 0.25, 0.5, 0.5, 0.25, 0.75, 1.0, 0.25, 0.25, None]

    def test_nonrealtime(self):
        session = nonrealtimetools.Session()
        with session.at(10):
            self.pattern.inscribe(session)
        assert session.to_lists() == [
            [10.0, [
                ['/d_recv', bytearray(
                    synthdeftools.SynthDefCompiler.compile_synthdefs([
                        synthdefs.system_link_audio_2,
                        synthdefs.default,
                        ]))],
                ['/g_new', 1000, 0, 0],
                ['/s_new', '454b69a7c505ddecc5b39762d291a5ec', 1001, 3, 1000,
                    'in_', 'a4'],
                ['/g_new', 1002, 1, 1000],
                ['/g_new', 1003, 1, 1000],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1002,
                    'amplitude', 1.0, 'frequency', 440, 'out', 4],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 222, 'out', 4]]],
            [10.75, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1003,
                    'amplitude', 1.0, 'frequency', 333, 'out', 4],
                ['/n_set', 1005, 'gate', 0]]],
            [11.0, [
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 660, 'out', 4]]],
            [11.5, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1007, 0, 1003,
                    'amplitude', 1.0, 'frequency', 444, 'out', 4],
                ['/n_set', 1006, 'gate', 0]]],
            [12.0, [
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 880, 'out', 4]]],
            [12.25, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1008, 0, 1003,
                    'amplitude', 1.0, 'frequency', 555, 'out', 4],
                ['/n_set', 1007, 'gate', 0]]],
            [13.0, [
                ['/n_set', 1004, 'amplitude', 1.0, 'frequency', 990, 'out', 4],
                ['/n_set', 1008, 'gate', 0]]],
            [14.0, [
                ['/n_set', 1004, 'gate', 0]]],
            [14.25, [
                ['/n_free', 1002, 1003]]],
            [14.5, [
                ['/n_free', 1000],
                ['/n_set', 1001, 'gate', 0],
                [0]]]]
