import supriya.osc
import supriya.realtime
import supriya.assets.synthdefs
from supriya import systemtools


class Test(systemtools.TestCase):

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_01(self):

        group_a = supriya.realtime.Group().allocate()
        group_b = supriya.realtime.Group().allocate()

        synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)

        group_a.append(synth_a)
        group_b.append(synth_b)

        remote_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 group
                        1003 test
                    1000 group
                        1002 test
            ''',
            )
        local_state = str(self.server.query_local_nodes())
        assert local_state == remote_state

        osc_message = supriya.osc.OscMessage(
            '/n_after',
            synth_b.node_id,
            synth_a.node_id,
            )
        self.server.send_message(osc_message)

        remote_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 group
                    1000 group
                        1002 test
                        1003 test
            ''',
            )
        local_state = str(self.server.query_local_nodes())
        assert local_state == remote_state

        osc_message = supriya.osc.OscMessage(
            '/n_order',
            0,
            group_b.node_id,
            synth_b.node_id,
            synth_a.node_id,
            )
        self.server.send_message(osc_message)

        remote_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            remote_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 group
                        1003 test
                        1002 test
                    1000 group
            ''',
            )
        local_state = str(self.server.query_local_nodes())
        assert local_state == remote_state
