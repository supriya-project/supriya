import uqbar.strings

import supriya.assets.synthdefs
import supriya.realtime


def test_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate(target_node=server)

    group_b = supriya.realtime.Group()
    group_b.allocate(target_node=server)

    synthdef = supriya.assets.synthdefs.test
    assert synthdef not in server

    synth_a = supriya.realtime.Synth(synthdef)
    assert synthdef not in server
    assert not synth_a.is_allocated

    group_a.append(synth_a)
    assert synthdef in server
    assert synth_a.is_allocated
    assert synth_a.parent is group_a
    assert synth_a in group_a
    assert synth_a not in group_b

    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
        """
    )

    group_b.append(synth_a)
    assert synthdef in server
    assert synth_a.is_allocated
    assert synth_a.parent is group_b
    assert synth_a in group_b
    assert synth_a not in group_a

    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1002 test
                1000 group
        """
    )

    synth_b = supriya.realtime.Synth(synthdef)
    assert not synth_b.is_allocated
    assert synth_b.parent is None

    group_b.append(synth_b)
    assert synth_b.is_allocated
    assert synth_b.parent is group_b

    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1002 test
                    1003 test
                1000 group
        """
    )
