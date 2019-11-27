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
            graph [bgcolor=transparent,
                color=lightslategrey,
                dpi=72,
                fontname=Arial,
                outputorder=edgesfirst,
                overlap=prism,
                penwidth=2,
                rankdir=TB,
                ranksep=0.5,
                splines=spline,
                style="dotted, rounded"];
            node [fontname=Arial,
                fontsize=12,
                penwidth=2,
                shape=Mrecord,
                style="filled, rounded"];
            edge [penwidth=2];
            group [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0 }"];
            "synth-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-0 }"];
            "group-1" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0-1 }"];
            "synth-1-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-1-0 }"];
            "synth-2" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-2 }"];
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
            graph [bgcolor=transparent,
                color=lightslategrey,
                dpi=72,
                fontname=Arial,
                outputorder=edgesfirst,
                overlap=prism,
                penwidth=2,
                rankdir=TB,
                ranksep=0.5,
                splines=spline,
                style="dotted, rounded"];
            node [fontname=Arial,
                fontsize=12,
                penwidth=2,
                shape=Mrecord,
                style="filled, rounded"];
            edge [penwidth=2];
            "group-1000" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 1000 }"];
            "synth-1001" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 1001 }"];
            "group-1002" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 1002 }"];
            "synth-1003" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 1003 }"];
            "synth-1004" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 1004 }"];
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
            graph [bgcolor=transparent,
                color=lightslategrey,
                dpi=72,
                fontname=Arial,
                outputorder=edgesfirst,
                overlap=prism,
                penwidth=2,
                rankdir=TB,
                ranksep=0.5,
                splines=spline,
                style="dotted, rounded"];
            node [fontname=Arial,
                fontsize=12,
                penwidth=2,
                shape=Mrecord,
                style="filled, rounded"];
            edge [penwidth=2];
            group [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0 }"];
            "synth-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-0 }"];
            "group-1" [fillcolor=lightsteelblue2,
                label="{ <f_0_0> Group | <f_0_1> id: 0-1 }"];
            "synth-1-0" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-1-0 }"];
            "synth-2" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0-2 }"];
            group -> "synth-0";
            group -> "group-1";
            group -> "synth-2";
            "group-1" -> "synth-1-0";
        }
        """
    )
