import uqbar.strings

import supriya.assets.synthdefs
import supriya.realtime


def test_01(server):
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_a.allocate()
    synth_b.allocate()
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 test
                1000 test
        """
    )
    synth_a.replace_with(synth_c)
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 test
                1002 test
        """
    )
    synth_b.replace_with([synth_d, synth_e])
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1003 test
                1004 test
                1002 test
        """
    )
    synth_c.replace_with([synth_a, synth_e])
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1003 test
                1005 test
                1004 test
        """
    )
