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

        group = servertools.Group().allocate()

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
            ''',
            ), server_state

        synth_a = servertools.Synth(synthdefs.test)
        group.insert(0, synth_a)

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
            ''',
            ), server_state

        synth_b = servertools.Synth(synthdefs.test)
        group.insert(0, synth_b)

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 test
                        1001 test
            ''',
            ), server_state

        synth_c = servertools.Synth(synthdefs.test)
        group.insert(1, synth_c)

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 test
                        1003 test
                        1001 test
            ''',
            ), server_state

        synth_d = servertools.Synth(synthdefs.test)
        group.insert(3, synth_d)

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 test
                        1003 test
                        1001 test
                        1004 test
            ''',
            ), server_state
