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

        synthdef = synthdefs.test
        assert not synthdef.is_allocated

        synth_a = servertools.Synth(synthdef)
        assert not synthdef.is_allocated
        assert not synth_a.is_allocated

        group_a.append(synth_a)
        assert synthdef.is_allocated
        assert synth_a.is_allocated
        assert synth_a.parent is group_a
        assert synth_a in group_a
        assert synth_a not in group_b

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 group
                    1000 group
                        1002 test
            ''',
            ), server_state

        group_b.append(synth_a)
        assert synthdef.is_allocated
        assert synth_a.is_allocated
        assert synth_a.parent is group_b
        assert synth_a in group_b
        assert synth_a not in group_a

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 group
                        1002 test
                    1000 group
            ''',
            ), server_state

        synth_b = servertools.Synth(synthdef)
        assert not synth_b.is_allocated
        assert synth_b.parent is None

        group_b.append(synth_b)
        assert synth_b.is_allocated
        assert synth_b.parent is group_b

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 group
                        1002 test
                        1003 test
                    1000 group
            ''',
            ), server_state
