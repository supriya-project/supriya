# -*- encoding: utf-8 -*-
import time
import types
import unittest
from abjad.tools import stringtools
from supriya import synthdefs
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(unittest.TestCase):

    pattern = patterntools.Pbus(
        pattern=patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        release_time=0.25,
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

    def test_manual_incommunicado_pbus_01(self):
        lists, deltas = self.manual_incommunicado(self.pattern)
        assert lists == [
            [10, [
                ['/g_new', 1000, 0, 1],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 3, 1000,
                    'amplitude', 1.0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440, 'out', 0]]],
            [11.0, [
                ['/n_set', 1002, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1000,
                    'amplitude', 1.0, 'frequency', 660, 'out', 0]]],
            [13.0, [
                ['/n_set', 1003, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1000,
                    'amplitude', 1.0, 'frequency', 880, 'out', 0]]],
            [16.0, [
                ['/n_set', 1004, 'gate', 0]]],
            [16.25, [
                ['/n_free', 1000, 1001]]]]
        assert deltas == [1.0, 2.0, 3.0, 0.25, None]

    def test_manual_communicado_pbind_01(self):
        player = patterntools.RealtimeEventPlayer(
            self.pattern,
            server=self.server,
            )
        # Initial State
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')
        # Step 1
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 2
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1003 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                        1002 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1003 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 3
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1004 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
                        1003 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1004 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 4
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1004 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 880.0, gate: 0.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 4
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == stringtools.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')
