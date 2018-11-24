import supriya.realtime
import supriya.assets.synthdefs
import uqbar.strings


def test_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate()

    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)

    group_b = supriya.realtime.Group()
    group_a.append(group_b)

    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)

    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)

    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                    1005 test
        '''
    )

    assert group_a.index(synth_a) == 0
    assert group_a.index(group_b) == 1
    assert group_a.index(synth_d) == 2
    assert group_b.index(synth_b) == 0
    assert group_b.index(synth_c) == 1
