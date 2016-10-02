# -*- encoding: utf-8 -*-
import time
import types
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(systemtools.TestCase):

    pbind_01 = patterntools.Pbind(
        amplitude=1.0,
        duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
        frequency=patterntools.Pseq([440, 660, 880], 1),
        )

    pbind_02 = patterntools.Pbind(
        amplitude=1.0,
        duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
        frequency=patterntools.Pseq([[440, 550], [550, 660], [660, 770]]),
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

    def test_manual_incommunicado_pbind_01(self):
        lists, deltas = self.manual_incommunicado(self.pbind_01)
        assert lists == [
            [10, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 1,
                    'amplitude', 1.0, 'frequency', 440]]],
            [11.0, [
                ['/n_set', 1000, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 1,
                    'amplitude', 1.0, 'frequency', 660]]],
            [13.0, [
                ['/n_set', 1001, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1,
                    'amplitude', 1.0, 'frequency', 880]]],
            [16.0, [
                ['/n_set', 1002, 'gate', 0]]]]
        assert deltas == [1.0, 2.0, 3.0, None]

    def test_manual_communicado_pbind_01(self):
        player = patterntools.RealtimeEventPlayer(
            self.pbind_01,
            server=self.server,
            )
        # Initial State
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')
        # Step 1
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 2
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                    1000 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
        ''')
        # Step 3
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
        ''')
        # Step 4
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')

    def test_automatic_communicado_pbind_01(self):
        self.pbind_01.play(server=self.server)
        time.sleep(6)

    def test_manual_incommunicado_pbind_02(self):
        lists, deltas = self.manual_incommunicado(self.pbind_02)
        assert lists == [
            [10, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 1,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 1,
                    'amplitude', 1.0, 'frequency', 550]]],
            [11.0, [
                ['/n_set', 1000, 'gate', 0],
                ['/n_set', 1001, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1,
                    'amplitude', 1.0, 'frequency', 550],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1,
                    'amplitude', 1.0, 'frequency', 660]]],
            [13.0, [
                ['/n_set', 1002, 'gate', 0],
                ['/n_set', 1003, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1,
                    'amplitude', 1.0, 'frequency', 660],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1,
                    'amplitude', 1.0, 'frequency', 770]]],
            [16.0, [
                ['/n_set', 1004, 'gate', 0],
                ['/n_set', 1005, 'gate', 0]]]]
        assert deltas == [1.0, 2.0, 3.0, None]

    def test_manual_communicado_pbind_02(self):
        player = patterntools.RealtimeEventPlayer(
            self.pbind_02,
            server=self.server,
            )
        # Initial State
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')
        # Step 1
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
                    1000 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 2
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1003 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 0.0, pan: 0.5
                    1000 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1003 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
        ''')
        # Step 3
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1005 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 770.0, gate: 1.0, pan: 0.5
                    1004 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                    1003 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1005 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 770.0, gate: 1.0, pan: 0.5
                    1004 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
        ''')
        # Step 4
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1005 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 770.0, gate: 0.0, pan: 0.5
                    1004 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')

    def test_automatic_communicado_pbind_02(self):
        self.pbind_02.play(server=self.server)
        time.sleep(6)

    def test_nonrealtime_01(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            self.pbind_01.inscribe(session)
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 0,
                    'amplitude', 1.0, 'frequency', 440]]],
            [1.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 0,
                    'amplitude', 1.0, 'frequency', 660],
                ['/n_set', 1000, 'gate', 0]]],
            [3.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 0,
                    'amplitude', 1.0, 'frequency', 880],
                ['/n_set', 1001, 'gate', 0]]],
            [6.0, [
                ['/n_set', 1002, 'gate', 0],
                [0]]],
            ]

    def test_nonrealtime_02(self):
        session = nonrealtimetools.Session()
        with session.at(10):
            self.pbind_02.inscribe(session)
        assert session.to_lists() == [
            [10.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 0,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 0,
                    'amplitude', 1.0, 'frequency', 550]]],
            [11.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 0,
                    'amplitude', 1.0, 'frequency', 550],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 0,
                    'amplitude', 1.0, 'frequency', 660],
                ['/n_set', 1000, 'gate', 0],
                ['/n_set', 1001, 'gate', 0]]],
            [13.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 0,
                    'amplitude', 1.0, 'frequency', 660],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 0,
                    'amplitude', 1.0, 'frequency', 770],
                ['/n_set', 1002, 'gate', 0],
                ['/n_set', 1003, 'gate', 0]]],
            [16.0, [
                ['/n_set', 1004, 'gate', 0],
                ['/n_set', 1005, 'gate', 0],
                [0]]]]

    def test_manual_stop_pbind_01(self):
        # Initial State
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')
        player = self.pbind_01.play(server=self.server)
        time.sleep(2)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
        ''')
        player.stop()
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1001 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')

    def test_manual_stop_pbind_02(self):
        # Initial State
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')
        player = self.pbind_02.play(server=self.server)
        time.sleep(2)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1003 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 1.0, pan: 0.5
        ''')
        player.stop()
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1003 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
                    1002 da0982184cc8fa54cf9d288a0fe1f6ca
                        out: 0.0, amplitude: 1.0, frequency: 550.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')
