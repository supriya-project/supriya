import pytest

import supriya.nonrealtime


def test_01():
    """
    With Session.at(...) context manager.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group_one = session.add_group()
        group_two = session.add_group()
        node = group_one.add_synth()
    with session.at(10):
        group_two.move_node(node)
    with session.at(5):
        parent = node.get_parent()
    assert parent is group_one
    with session.at(15):
        parent = node.get_parent()
    assert parent is group_two


def test_02():
    """
    With offset=... keyword.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group_one = session.add_group()
        group_two = session.add_group()
        node = group_one.add_synth()
    with session.at(10):
        group_two.move_node(node)
    parent = node.get_parent(offset=5)
    assert parent is group_one
    parent = node.get_parent(offset=15)
    assert parent is group_two


def test_03():
    """
    Without Session.at(...) context manager or offset keyword.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group_one = session.add_group()
        group_two = session.add_group()
        node = group_one.add_synth()
    with session.at(10):
        group_two.move_node(node)
    with pytest.raises(ValueError):
        node.get_parent()


def test_04():
    """
    With both Session.at(...) context manager and offset keyword.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        group_one = session.add_group()
        group_two = session.add_group()
        node = group_one.add_synth()
    with session.at(10):
        group_two.move_node(node)
    with session.at(5):
        parent = node.get_parent(offset=15)
    assert parent is group_two
