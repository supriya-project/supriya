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
        group_a.allocate()

        assert len(group_a) == 0

        synth_a = servertools.Synth(synthdefs.test)
        group_a.append(synth_a)

        assert len(group_a) == 1

        group_b = servertools.Group()
        group_a.append(group_b)

        assert len(group_a) == 2
        assert len(group_b) == 0

        synth_b = servertools.Synth(synthdefs.test)
        group_b.append(synth_b)

        assert len(group_a) == 2
        assert len(group_b) == 1

        synth_c = servertools.Synth(synthdefs.test)
        group_b.append(synth_c)

        assert len(group_a) == 2
        assert len(group_b) == 2

        synth_d = servertools.Synth(synthdefs.test)
        group_a.append(synth_d)

        assert len(group_a) == 3
        assert len(group_b) == 2

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            """
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
                        1002 group
                            1003 test
                            1004 test
                        1005 test
            """,
            ), server_state

        assert len(group_a) == 3
        assert len(group_b) == 2

        group_a.pop()

        assert len(group_a) == 2

        group_b.pop()

        assert len(group_b) == 1

        group_a.pop()

        assert len(group_a) == 1
        assert len(group_b) == 1
        assert not group_b[0].is_allocated

        group_a.pop()

        assert len(group_a) == 0

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            """
            NODE TREE 0 group
                1 group
                    1000 group
            """,
            ), server_state
