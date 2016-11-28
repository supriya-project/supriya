# -*- encoding: utf-8 -*-
import time
from patterntools_testbase import TestCase
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools
from supriya.tools import synthdeftools


class TestCase(TestCase):

    pattern = patterntools.Pbus(
        pattern=patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        release_time=0.25,
        )

    def test_manual_incommunicado(self):
        lists, deltas = self.manual_incommunicado(self.pattern)
        assert lists == [
            [10, [
                ['/g_new', 1000, 0, 1],
                ['/s_new', '454b69a7c505ddecc5b39762d291a5ec', 1001, 3, 1000,
                    'in_', 0],
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
                    1000 group
                        1002 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
                    1001 454b69a7c505ddecc5b39762d291a5ec
                        done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        ''')
        # Step 2
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1003 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                        1002 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 440.0, gate: 0.0, pan: 0.5
                    1001 454b69a7c505ddecc5b39762d291a5ec
                        done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1003 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
                    1001 454b69a7c505ddecc5b39762d291a5ec
                        done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        ''')
        # Step 3
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1004 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
                        1003 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 660.0, gate: 0.0, pan: 0.5
                    1001 454b69a7c505ddecc5b39762d291a5ec
                        done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1004 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
                    1001 454b69a7c505ddecc5b39762d291a5ec
                        done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        ''')
        # Step 4
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                        1004 da0982184cc8fa54cf9d288a0fe1f6ca
                            out: 16.0, amplitude: 1.0, frequency: 880.0, gate: 0.0, pan: 0.5
                    1001 454b69a7c505ddecc5b39762d291a5ec
                        done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
                    1000 group
                    1001 454b69a7c505ddecc5b39762d291a5ec
                        done_action: 2.0, fade_time: 0.02, gate: 1.0, in_: 16.0, out: 0.0
        ''')
        # Step 4
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
            NODE TREE 0 group
                1 group
        ''')

    def test_nonrealtime(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            self.pattern.inscribe(session)
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(
                    synthdeftools.SynthDefCompiler.compile_synthdefs([
                        synthdefs.system_link_audio_2,
                        synthdefs.default,
                        ]))],
                ['/g_new', 1000, 0, 0],
                ['/s_new', '454b69a7c505ddecc5b39762d291a5ec', 1001, 3, 1000,
                    'in_', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16]]],
            [1.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1000,
                    'amplitude', 1.0, 'frequency', 660, 'out', 16],
                ['/n_set', 1002, 'gate', 0]]],
            [3.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1000,
                    'amplitude', 1.0, 'frequency', 880, 'out', 16],
                ['/n_set', 1003, 'gate', 0]]],
            [6.0, [['/n_set', 1004, 'gate', 0]]],
            [6.25, [['/n_free', 1000], ['/n_set', 1001, 'gate', 0], [0]]]]

    def test_send_01(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(4):
            events.append(next(iterator))
        iterator.send(True)
        events.extend(iterator)
        assert [
            (type(x).__name__, x.get('is_stop') or False)
            for x in events] == [
            ('BusEvent', False),
            ('GroupEvent', False),
            ('SynthEvent', False),
            ('NoteEvent', True),
            ('SynthEvent', True),
            ('GroupEvent', True),
            ('BusEvent', True),
            ]

    def test_send_02(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(3):
            events.append(next(iterator))
        iterator.send(True)
        events.extend(iterator)
        assert [
            (type(x).__name__, x.get('is_stop') or False)
            for x in events] == [
            ('BusEvent', False),
            ('GroupEvent', False),
            ('SynthEvent', False),
            ('SynthEvent', True),
            ('GroupEvent', True),
            ('BusEvent', True),
            ]

    def test_send_03(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(2):
            events.append(next(iterator))
        iterator.send(True)
        events.extend(iterator)
        assert [
            (type(x).__name__, x.get('is_stop') or False)
            for x in events] == [
            ('BusEvent', False),
            ('GroupEvent', False),
            ('GroupEvent', True),
            ('BusEvent', True),
            ]

    def test_send_04(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(1):
            events.append(next(iterator))
        iterator.send(True)
        events.extend(iterator)
        assert [
            (type(x).__name__, x.get('is_stop') or False)
            for x in events] == [
            ('BusEvent', False),
            ('BusEvent', True),
            ]
