import supriya.nonrealtime
import supriya.realtime


def test_add_to_head_01():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(2)]
    nodes_to_children = {nodes[0]: None}
    nodes_to_parents = {nodes[0]: None}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[1], target=nodes[0], action=supriya.AddAction.ADD_TO_HEAD
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {nodes[0]: (nodes[1],), nodes[1]: None}
    assert nodes_to_parents == {nodes[0]: None, nodes[1]: nodes[0]}


def test_add_to_head_02():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(4)]
    nodes_to_children = {
        nodes[0]: (nodes[1], nodes[2]),
        nodes[1]: None,
        nodes[2]: (nodes[3],),
        nodes[3]: None,
    }
    nodes_to_parents = {
        nodes[0]: None,
        nodes[1]: nodes[0],
        nodes[2]: nodes[0],
        nodes[3]: nodes[2],
    }
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[3], target=nodes[1], action=supriya.AddAction.ADD_TO_HEAD
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[1], nodes[2]),
        nodes[1]: (nodes[3],),
        nodes[2]: None,
        nodes[3]: None,
    }
    assert nodes_to_parents == {
        nodes[0]: None,
        nodes[1]: nodes[0],
        nodes[2]: nodes[0],
        nodes[3]: nodes[1],
    }


def test_add_to_head_03():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(3)]
    nodes_to_children = {nodes[0]: (nodes[1], nodes[2]), nodes[1]: None, nodes[2]: None}
    nodes_to_parents = {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[2], target=nodes[0], action=supriya.AddAction.ADD_TO_HEAD
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[2], nodes[1]),
        nodes[1]: None,
        nodes[2]: None,
    }
    assert nodes_to_parents == {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}


def test_add_to_head_04():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(3)]
    nodes_to_children = {nodes[0]: (nodes[1], nodes[2]), nodes[1]: None, nodes[2]: None}
    nodes_to_parents = {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[1], target=nodes[0], action=supriya.AddAction.ADD_TO_HEAD
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[1], nodes[2]),
        nodes[1]: None,
        nodes[2]: None,
    }
    assert nodes_to_parents == {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}


def test_add_to_tail_01():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(2)]
    nodes_to_children = {nodes[0]: None}
    nodes_to_parents = {nodes[0]: None}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[1], target=nodes[0], action=supriya.AddAction.ADD_TO_TAIL
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {nodes[0]: (nodes[1],), nodes[1]: None}
    assert nodes_to_parents == {nodes[0]: None, nodes[1]: nodes[0]}


def test_add_to_tail_02():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(4)]
    nodes_to_children = {
        nodes[0]: (nodes[1], nodes[2]),
        nodes[1]: None,
        nodes[2]: (nodes[3],),
        nodes[3]: None,
    }
    nodes_to_parents = {
        nodes[0]: None,
        nodes[1]: nodes[0],
        nodes[2]: nodes[0],
        nodes[3]: nodes[2],
    }
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[3], target=nodes[1], action=supriya.AddAction.ADD_TO_TAIL
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[1], nodes[2]),
        nodes[1]: (nodes[3],),
        nodes[2]: None,
        nodes[3]: None,
    }
    assert nodes_to_parents == {
        nodes[0]: None,
        nodes[1]: nodes[0],
        nodes[2]: nodes[0],
        nodes[3]: nodes[1],
    }


def test_add_to_tail_03():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(3)]
    nodes_to_children = {nodes[0]: (nodes[1], nodes[2]), nodes[1]: None, nodes[2]: None}
    nodes_to_parents = {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[1], target=nodes[0], action=supriya.AddAction.ADD_TO_TAIL
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[2], nodes[1]),
        nodes[1]: None,
        nodes[2]: None,
    }
    assert nodes_to_parents == {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}


def test_add_to_tail_04():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(3)]
    nodes_to_children = {nodes[0]: (nodes[1], nodes[2]), nodes[1]: None, nodes[2]: None}
    nodes_to_parents = {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[2], target=nodes[0], action=supriya.AddAction.ADD_TO_TAIL
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[1], nodes[2]),
        nodes[1]: None,
        nodes[2]: None,
    }
    assert nodes_to_parents == {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}


def test_add_before_01():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(4)]
    nodes_to_children = {nodes[0]: (nodes[1], nodes[2]), nodes[1]: None, nodes[2]: None}
    nodes_to_parents = {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[3], target=nodes[2], action=supriya.AddAction.ADD_BEFORE
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[1], nodes[3], nodes[2]),
        nodes[1]: None,
        nodes[2]: None,
        nodes[3]: None,
    }
    assert nodes_to_parents == {
        nodes[0]: None,
        nodes[1]: nodes[0],
        nodes[2]: nodes[0],
        nodes[3]: nodes[0],
    }


def test_add_after_01():
    nodes = [supriya.nonrealtime.Group(None, i) for i in range(4)]
    nodes_to_children = {nodes[0]: (nodes[1], nodes[2]), nodes[1]: None, nodes[2]: None}
    nodes_to_parents = {nodes[0]: None, nodes[1]: nodes[0], nodes[2]: nodes[0]}
    action = supriya.nonrealtime.NodeTransition(
        source=nodes[3], target=nodes[1], action=supriya.AddAction.ADD_AFTER
    )
    action.apply_transform(nodes_to_children, nodes_to_parents)
    assert nodes_to_children == {
        nodes[0]: (nodes[1], nodes[3], nodes[2]),
        nodes[1]: None,
        nodes[2]: None,
        nodes[3]: None,
    }
    assert nodes_to_parents == {
        nodes[0]: None,
        nodes[1]: nodes[0],
        nodes[2]: nodes[0],
        nodes[3]: nodes[0],
    }
