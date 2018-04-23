import supriya.realtime
import supriya.assets.synthdefs
import uqbar.strings


def test_Node_parentage_01(server):

    root_node = server.root_node
    default_group = server.default_group

    group_a = supriya.realtime.Group().allocate()
    group_b = supriya.realtime.Group().allocate(target_node=group_a)
    group_c = supriya.realtime.Group().allocate(target_node=group_b)
    group_d = supriya.realtime.Group().allocate(target_node=group_c)
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_d.extend([synth_a, synth_b])

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1002 group
                            1003 group
                                1004 test
                                1005 test
        ''')

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

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
                        1002 group
                1003 group
                    1004 test
                    1005 test
        ''')

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
