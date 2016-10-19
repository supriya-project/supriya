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

        group_a = servertools.Group()
        group_a.allocate(target_node=self.server)

        group_b = servertools.Group()
        group_b.allocate(target_node=self.server)

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            """
            NODE TREE 0 group
                1 group
                    1001 group
                    1000 group
            """,
            ), server_state

        synthdef = synthdefs.test
        assert not synthdef.is_allocated

        synth_a = servertools.Synth(synthdef)
        synth_b = servertools.Synth(synthdef)
        synth_c = servertools.Synth(synthdef)
        synth_d = servertools.Synth(synthdef)

        assert not synth_a.is_allocated
        assert not synth_b.is_allocated
        assert not synth_c.is_allocated
        assert not synth_d.is_allocated

        synth_a.allocate()

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            """
            NODE TREE 0 group
                1 group
                    1002 test
                    1001 group
                    1000 group
            """,
            ), server_state

        group_a.extend([synth_a, synth_b])

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            """
            NODE TREE 0 group
                1 group
                    1001 group
                    1000 group
                        1002 test
                        1003 test
            """,
            ), server_state

        group_b.extend([synth_c])

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            """
            NODE TREE 0 group
                1 group
                    1001 group
                        1004 test
                    1000 group
                        1002 test
                        1003 test
            """,
            ), server_state

        group_b.extend([synth_d, synth_b, synth_a])

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            """
            NODE TREE 0 group
                1 group
                    1001 group
                        1004 test
                        1005 test
                        1003 test
                        1002 test
                    1000 group
            """,
            ), server_state
