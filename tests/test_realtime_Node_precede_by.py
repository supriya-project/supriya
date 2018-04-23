import supriya.assets.synthdefs
import supriya.realtime
import uqbar.strings


def test_01(server):
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_a.allocate()
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1000 test
        ''')
    synth_a.precede_by(synth_b)
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 test
                1000 test
        ''')
    synth_a.precede_by([synth_c, synth_d])
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1001 test
                1002 test
                1003 test
                1000 test
        ''')
    synth_a.precede_by([synth_e, synth_b])
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize('''
        NODE TREE 0 group
            1 group
                1002 test
                1003 test
                1004 test
                1001 test
                1000 test
        ''')
