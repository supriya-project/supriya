from uqbar.strings import normalize

from supriya import Server, default


def test_QueryTreeGroup_annotate() -> None:
    server = Server().boot()
    server.add_synthdefs(default)
    server.sync()
    group_a = server.add_group()
    group_b = group_a.add_group()
    group_a.add_synth(synthdef=default)
    group_b.add_synth(synthdef=default)
    group_b.add_synth(synthdef=default)
    group_b.add_group()
    tree = server.query_tree()
    assert tree is not None
    assert str(tree) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1001 group
                        1005 group
                        1004 supriya:default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                        1003 supriya:default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
    assert str(tree.annotate({})) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1002 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1001 group
                        1005 group
                        1004 supriya:default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                        1003 supriya:default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
    assert str(
        tree.annotate(
            {
                0: "root",
                1: "default group",
                1000: "mixer",
                1005: "grandchild",
                1003: "synth",
            }
        )
    ) == normalize(
        """
        NODE TREE 0 group (root)
            1 group (default group)
                1000 group (mixer)
                    1002 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1001 group
                        1005 group (grandchild)
                        1004 supriya:default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                        1003 supriya:default (synth)
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
