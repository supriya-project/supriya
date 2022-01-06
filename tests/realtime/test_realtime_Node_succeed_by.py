import uqbar.strings

import supriya.assets.synthdefs
import supriya.realtime


def test_01(server):
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_a.allocate(server)
    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
        """
    )
    synth_a.succeed_by(synth_b)
    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
                1001 test
        """
    )
    synth_a.succeed_by([synth_c, synth_d])
    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
                1002 test
                1003 test
                1001 test
        """
    )
    synth_a.succeed_by([synth_e, synth_b])
    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 test
                1004 test
                1001 test
                1002 test
                1003 test
        """
    )
