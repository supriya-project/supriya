import uqbar.strings

import supriya


def test_01(server):
    synth = supriya.Synth()
    assert format(synth.__graph__(), "graphviz") == uqbar.strings.normalize(
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
            synth [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0 }"];
        }
        """
    )
    synth.allocate(server)
    assert format(synth.__graph__(), "graphviz") == uqbar.strings.normalize(
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
            "synth-1000" [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 1000 }"];
        }
        """
    )
    synth.free()
    assert format(synth.__graph__(), "graphviz") == uqbar.strings.normalize(
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
            synth [fillcolor=lightgoldenrod2,
                label="{ <f_0_0> Synth | <f_0_1> id: 0 }"];
        }
        """
    )
