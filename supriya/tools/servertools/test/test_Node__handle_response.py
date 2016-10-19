# -*- encoding: utf-8 -*-
import os
import unittest
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import osctools
from supriya.tools import servertools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No Scsynth on Travis-CI')
class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server().boot()

    def tearDown(self):
        self.server.quit()

    def test_01(self):

        group_a = servertools.Group().allocate()
        group_b = servertools.Group().allocate()

        synth_a = servertools.Synth(synthdefs.test)
        synth_b = servertools.Synth(synthdefs.test)

        group_a.append(synth_a)
        group_b.append(synth_b)

        remote_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            remote_state,
            """
            NODE TREE 0 group
                1 group
                    1001 group
                        1003 test
                    1000 group
                        1002 test
            """,
            ), remote_state
        local_state = str(self.server.query_local_nodes())
        assert local_state == remote_state

        osc_message = osctools.OscMessage(
            '/n_after',
            synth_b.node_id,
            synth_a.node_id,
            )
        self.server.send_message(osc_message)

        remote_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            remote_state,
            """
            NODE TREE 0 group
                1 group
                    1001 group
                    1000 group
                        1002 test
                        1003 test
            """,
            ), remote_state
        local_state = str(self.server.query_local_nodes())
        assert local_state == remote_state

        osc_message = osctools.OscMessage(
            '/n_order',
            0,
            group_b.node_id,
            synth_b.node_id,
            synth_a.node_id,
            )
        self.server.send_message(osc_message)

        remote_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            remote_state,
            """
            NODE TREE 0 group
                1 group
                    1001 group
                        1003 test
                        1002 test
                    1000 group
            """,
            ), remote_state
        local_state = str(self.server.query_local_nodes())
        assert local_state == remote_state
