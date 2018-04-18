import supriya.realtime
import supriya.assets.synthdefs
import uqbar.strings


def test_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(target_node=server)

    group_b = supriya.realtime.Group()
    group_b.allocate(target_node=server)

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
        ''')

    synthdef = supriya.assets.synthdefs.test
    assert not synthdef.is_allocated

    synth_a = supriya.realtime.Synth(synthdef)
    synth_b = supriya.realtime.Synth(synthdef)
    synth_c = supriya.realtime.Synth(synthdef)
    synth_d = supriya.realtime.Synth(synthdef)

    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    assert not synth_c.is_allocated
    assert not synth_d.is_allocated

    synth_a.allocate()

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1002 test
                1001 group
                1000 group
        ''')

    group_a.extend([synth_a, synth_b])

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
                    1003 test
        ''')

    group_b.extend([synth_c])

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                1000 group
                    1002 test
                    1003 test
        ''')

    group_b.extend([synth_d, synth_b, synth_a])

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                    1005 test
                    1003 test
                    1002 test
                1000 group
        ''')
