import supriya.realtime
from supriya import synthdefs
from supriya import systemtools


class Test(systemtools.TestCase):

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_Node_parentage_01(self):

        root_node = self.server.root_node
        default_group = self.server.default_group

        group_a = supriya.realtime.Group().allocate()
        group_b = supriya.realtime.Group().allocate(target_node=group_a)
        group_c = supriya.realtime.Group().allocate(target_node=group_b)
        group_d = supriya.realtime.Group().allocate(target_node=group_c)
        synth_a = supriya.realtime.Synth(synthdefs.test)
        synth_b = supriya.realtime.Synth(synthdefs.test)
        group_d.extend([synth_a, synth_b])

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 group
                            1002 group
                                1003 group
                                    1004 test
                                    1005 test
            ''',
            )

        assert group_a.parentage == (
            group_a,
            default_group,
            root_node,
            )

        assert group_b.parentage == (
            group_b,
            group_a,
            default_group,
            root_node,
            )

        assert group_c.parentage == (
            group_c,
            group_b,
            group_a,
            default_group,
            root_node,
            )

        assert group_d.parentage == (
            group_d,
            group_c,
            group_b,
            group_a,
            default_group,
            root_node,
            )

        assert synth_a.parentage == (
            synth_a,
            group_d,
            group_c,
            group_b,
            group_a,
            default_group,
            root_node,
            )

        assert synth_b.parentage == (
            synth_b,
            group_d,
            group_c,
            group_b,
            group_a,
            default_group,
            root_node,
            )

        group_a.succeed_by(group_d)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 group
                            1002 group
                    1003 group
                        1004 test
                        1005 test
            ''',
            )

        assert group_d.parentage == (
            group_d,
            default_group,
            root_node,
            )

        assert synth_a.parentage == (
            synth_a,
            group_d,
            default_group,
            root_node,
            )

        assert synth_b.parentage == (
            synth_b,
            group_d,
            default_group,
            root_node,
            )
