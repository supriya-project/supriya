import supriya.assets.synthdefs
import supriya.realtime
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
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        ''')

    assert group_a[0] is synth_a
    assert group_a[1] is group_b
    assert group_a[2] is synth_d

    assert group_b[0] is synth_b
    assert group_b[1] is synth_c
    assert group_b[2] is group_c

    assert group_a[-1] is synth_d
    assert group_a[-2] is group_b
    assert group_a[-3] is synth_a

    assert group_b[-1] is group_c
    assert group_b[-2] is synth_c
    assert group_b[-3] is synth_b

    assert group_a[:] == [synth_a, group_b, synth_d]
    assert group_a[1:] == [group_b, synth_d]
    assert group_a[1:-1] == [group_b]
    assert group_a[2:] == [synth_d]
    assert group_a[:-1] == [synth_a, group_b]
    assert group_a[:-2] == [synth_a]

    assert group_b[:] == [synth_b, synth_c, group_c]
    assert group_b[1:] == [synth_c, group_c]
    assert group_b[1:-1] == [synth_c]
    assert group_b[2:] == [group_c]
    assert group_b[:-1] == [synth_b, synth_c]
    assert group_b[:-2] == [synth_b]
