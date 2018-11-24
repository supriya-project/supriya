import uqbar.strings

import supriya.assets.synthdefs
import supriya.realtime


def test_01(server):
    group = supriya.realtime.Group().allocate()
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
        """
    )
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(0, synth_a)
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
        """
    )
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(0, synth_b)
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1001 test
        """
    )
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(1, synth_c)
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1003 test
                    1001 test
        """
    )
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group.insert(3, synth_d)
    server_state = str(server.query_remote_nodes())
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1003 test
                    1001 test
                    1004 test
        """
    )
