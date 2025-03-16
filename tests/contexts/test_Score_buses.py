import logging

import pytest

from supriya.contexts.errors import ContextError, InvalidCalculationRate
from supriya.contexts.nonrealtime import Score
from supriya.osc import OscBundle, OscMessage


@pytest.fixture(autouse=True)
def use_caplog(caplog) -> None:
    caplog.set_level(logging.INFO)


@pytest.fixture
def context() -> Score:
    return Score()


def test_add_bus(context: Score) -> None:
    # no moment
    with pytest.raises(ContextError):
        context.add_bus("AUDIO")
    with context.at(0):
        # invalid calculation rate
        with pytest.raises(InvalidCalculationRate):
            context.add_bus("SCALAR")
        # ok
        audio_bus = context.add_bus("AUDIO")
        control_bus = context.add_bus("CONTROL")
    assert audio_bus.context is context
    assert audio_bus.id_ == 16
    assert control_bus.context is context
    assert control_bus.id_ == 0
    assert list(context.iterate_osc_bundles()) == []


def test_add_bus_group(context: Score) -> None:
    # no moment
    with pytest.raises(ContextError):
        context.add_bus_group("AUDIO", 0)
    with context.at(0):
        # invalid calculation rate
        with pytest.raises(InvalidCalculationRate):
            context.add_bus_group("SCALAR")
        # count less than 1
        with pytest.raises(ValueError):
            context.add_bus_group("AUDIO", 0)
        # ok
        audio_bus_group = context.add_bus_group("AUDIO", 8)
        control_bus_group = context.add_bus_group("CONTROL", 4)
    assert len(audio_bus_group) == 8
    assert all(audio_bus.context is context for audio_bus in audio_bus_group)
    assert [audio_bus.id_ for audio_bus in audio_bus_group] == [
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
    ]
    assert len(control_bus_group) == 4
    assert all(control_bus.context is context for control_bus in control_bus_group)
    assert [control_bus.id_ for control_bus in control_bus_group] == [0, 1, 2, 3]
    assert list(context.iterate_osc_bundles()) == []


def test_fill_buses(context: Score) -> None:
    with context.at(0):
        audio_bus = context.add_bus("AUDIO")
        control_bus_a = context.add_bus("CONTROL")
        control_bus_b = context.add_bus("CONTROL")
        control_bus_c = context.add_bus("CONTROL")
        with pytest.raises(InvalidCalculationRate):
            audio_bus.fill(2, 0.75)
        control_bus_a.fill(3, 0.5)
    with context.at(1.23):
        control_bus_b.fill(4, 0.25)
        control_bus_c.fill(5, 0.125)
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(contents=(OscMessage("/c_fill", 0, 3, 0.5),), timestamp=0.0),
        OscBundle(
            contents=(OscMessage("/c_fill", 1, 4, 0.25, 2, 5, 0.125),), timestamp=1.23
        ),
    ]


def test_free_bus(context: Score) -> None:
    with context.at(0):
        audio_bus = context.add_bus("AUDIO")
        control_bus = context.add_bus("CONTROL")
        audio_bus.free()
        control_bus.free()
    assert list(context.iterate_osc_bundles()) == []
    with context.at(1.23):
        new_audio_bus = context.add_bus("AUDIO")
        new_control_bus = context.add_bus("CONTROL")
    # NRT contexts don't re-use IDs
    assert new_audio_bus.id_ == audio_bus.id_ + 1
    assert new_control_bus.id_ == control_bus.id_ + 1


def test_set_bus(context: Score) -> None:
    with context.at(0):
        audio_bus = context.add_bus("AUDIO")
        control_bus_a = context.add_bus("CONTROL")
        control_bus_b = context.add_bus("CONTROL")
        control_bus_c = context.add_bus("CONTROL")
        with pytest.raises(InvalidCalculationRate):
            audio_bus.set(0.75)
        control_bus_a.set(0.5)
    with context.at(1.23):
        control_bus_b.set(0.25)
        control_bus_c.set(0.125)
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(contents=(OscMessage("/c_set", 0, 0.5),), timestamp=0.0),
        OscBundle(contents=(OscMessage("/c_set", 1, 0.25, 2, 0.125),), timestamp=1.23),
    ]


@pytest.mark.asyncio
async def test_set_bus_range(context: Score) -> None:
    with context.at(0):
        audio_bus_group = context.add_bus_group("AUDIO", count=4)
        control_bus_group = context.add_bus_group("CONTROL", count=4)
    with context.at(1.23):
        with pytest.raises(InvalidCalculationRate):
            audio_bus_group[0].set_range((0.1, 0.2, 0.3, 0.4))
        control_bus_group[0].set_range((0.1, 0.2, 0.3, 0.4))
    assert list(context.iterate_osc_bundles()) == [
        OscBundle(
            contents=(OscMessage("/c_setn", 0, 4, 0.1, 0.2, 0.3, 0.4),), timestamp=1.23
        )
    ]
