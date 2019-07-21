import supriya.nonrealtime


def test_iterate_nodes():
    nodes = {
        "A": ["B", "C", "D"],
        "B": None,
        "C": ["E", "F"],
        "D": None,
        "E": ["G"],
        "F": None,
        "G": None,
    }
    root = "A"
    iterator = supriya.nonrealtime.State._iterate_nodes(root, nodes)
    assert list(iterator) == ["A", "B", "C", "E", "G", "F", "D"]
