import pytest

import supriya.assets.synthdefs
import supriya.nonrealtime


def test_01():
    """
    With Session.at(...) context manager.
    """
    session = supriya.nonrealtime.Session()
    with session.at(5):
        node = session.add_synth(duration=10)
    assert isinstance(node, supriya.nonrealtime.Synth)
    assert node in session.nodes
    assert node.start_offset == 5
    assert node.stop_offset == 15


def test_02():
    """
    With offset=... keyword.
    """
    session = supriya.nonrealtime.Session()
    node = session.add_synth(duration=10, offset=5)
    assert isinstance(node, supriya.nonrealtime.Synth)
    assert node in session.nodes
    assert node.start_offset == 5
    assert node.stop_offset == 15


def test_03():
    """
    Without Session.at(...) context manager or offset keyword.
    """
    session = supriya.nonrealtime.Session()
    with pytest.raises(ValueError):
        session.add_synth(duration=10)


def test_04():
    """
    With both Session.at(...) context manager and offset keyword.
    """
    session = supriya.nonrealtime.Session()
    with session.at(5):
        node = session.add_synth(duration=10, offset=13)
    assert isinstance(node, supriya.nonrealtime.Synth)
    assert node in session.nodes
    assert node.start_offset == 13
    assert node.stop_offset == 23


def test_05():
    """
    Mismatch.
    """
    session = supriya.nonrealtime.Session()
    with session.at(5):
        node = session.add_synth(duration=10, offset=13)
        with pytest.raises(ValueError):
            node.add_synth(duration=1)


def test_06():
    """
    Defaults.
    """
    session = supriya.nonrealtime.Session()
    with session.at(0):
        synth = session.add_synth()
    assert synth.synthdef == supriya.assets.synthdefs.default
    assert synth.duration == float("inf")
    assert synth.start_offset == 0.0
