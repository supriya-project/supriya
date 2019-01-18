import uqbar.strings

import supriya


def test_01(server):
    synth = supriya.Synth()
    assert format(synth.__graph__(), "graphviz") == uqbar.strings.normalize(
        """
        digraph G {
            synth;
        }
        """
    )
    synth.allocate()
    assert format(synth.__graph__(), "graphviz") == uqbar.strings.normalize(
        """
        digraph G {
            "synth-1000";
        }
        """
    )
    synth.free()
    assert format(synth.__graph__(), "graphviz") == uqbar.strings.normalize(
        """
        digraph G {
            synth;
        }
        """
    )
