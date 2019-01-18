import uqbar.strings

import supriya


def test_01(server):
    outer_group = supriya.Group()
    inner_group = supriya.Group()
    synth_a = supriya.Synth()
    synth_b = supriya.Synth()
    synth_c = supriya.Synth()
    outer_group.extend([synth_a, inner_group, synth_c])
    inner_group.append(synth_b)
    assert format(outer_group.__graph__(), "graphviz") == uqbar.strings.normalize(
        """
        digraph G {
            group;
            "synth-0";
            "group-1";
            "synth-1-0";
            "synth-2";
            group -> "synth-0";
            group -> "group-1";
            group -> "synth-2";
            "group-1" -> "synth-1-0";
        }
        """
    )
    outer_group.allocate()
    assert format(outer_group.__graph__(), "graphviz") == uqbar.strings.normalize(
        """
        digraph G {
            "group-1000";
            "synth-1001";
            "group-1002";
            "synth-1003";
            "synth-1004";
            "group-1000" -> "synth-1001";
            "group-1000" -> "group-1002";
            "group-1000" -> "synth-1004";
            "group-1002" -> "synth-1003";
        }
        """
    )
    outer_group.free()
    assert format(outer_group.__graph__(), "graphviz") == uqbar.strings.normalize(
        """
        digraph G {
            group;
            "synth-0";
            "group-1";
            "synth-1-0";
            "synth-2";
            group -> "synth-0";
            group -> "group-1";
            group -> "synth-2";
            "group-1" -> "synth-1-0";
        }
        """
    )
