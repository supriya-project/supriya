# -*- encoding: utf-8 -*-
import os
import unittest
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import servertools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No Scsynth on Travis-CI')
class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server().boot()

    def tearDown(self):
        self.server.quit()

    def test_01(self):

        group = servertools.Group()
        synth_a = servertools.Synth(synthdefs.test)
        synth_b = servertools.Synth(synthdefs.test, amplitude=0.0)
        group.extend([synth_a, synth_b])
        group.allocate()

        remote_state = str(self.server.query_remote_nodes(True))
        assert systemtools.TestManager.compare(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
                            amplitude: 1.0, frequency: 440.0
                        1002 test
                            amplitude: 0.0, frequency: 440.0
            ''',
            ), remote_state
        local_state = str(self.server.query_local_nodes(True))
        assert local_state == remote_state

        bus_a = servertools.Bus(calculation_rate='control').allocate()
        bus_a.set(0.25)
        group.controls['amplitude'] = bus_a

        remote_state = str(self.server.query_remote_nodes(True))
        assert systemtools.TestManager.compare(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
                            amplitude: c0, frequency: 440.0
                        1002 test
                            amplitude: c0, frequency: 440.0
            ''',
            ), remote_state
        local_state = str(self.server.query_local_nodes(True))
        assert local_state == remote_state

        bus_b = servertools.Bus(calculation_rate='control').allocate()
        bus_b.set(0.75)
        group.controls['amplitude'] = bus_b

        remote_state = str(self.server.query_remote_nodes(True))
        assert systemtools.TestManager.compare(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
                            amplitude: c1, frequency: 440.0
                        1002 test
                            amplitude: c1, frequency: 440.0
            ''',
            ), remote_state
        local_state = str(self.server.query_local_nodes(True))
        assert local_state == remote_state

        bus_b.set(0.675)

        remote_state = str(self.server.query_remote_nodes(True))
        assert systemtools.TestManager.compare(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
                            amplitude: c1, frequency: 440.0
                        1002 test
                            amplitude: c1, frequency: 440.0
            ''',
            ), remote_state
        local_state = str(self.server.query_local_nodes(True))
        assert local_state == remote_state

        group.controls['amplitude'] = None

        remote_state = str(self.server.query_remote_nodes(True))
        assert systemtools.TestManager.compare(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
                            amplitude: 1.0, frequency: 440.0
                        1002 test
                            amplitude: 0.0, frequency: 440.0
            ''',
            ), remote_state
        local_state = str(self.server.query_local_nodes(True))
        assert local_state == remote_state