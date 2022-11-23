from dataclasses import dataclass
from typing import Tuple

import hypothesis
import hypothesis.strategies as st
import pytest

import supriya.assets
import supriya.realtime
import supriya.synthdefs
from supriya import CalculationRate
from supriya.exceptions import BusNotAllocated, IncompatibleRate
from tests.proptest import get_control_test_groups, hp_global_settings


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


hp_settings = hypothesis.settings(
    hp_global_settings,
    deadline=1999,
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
)


@dataclass
class SampleBusGroup:
    bus_group: supriya.realtime.BusGroup
    calculation_rate: CalculationRate
    bus_count: int
    set_values: Tuple[float] = (0.0,)


@get_control_test_groups(max_size=64)
@st.composite
def st_bus_group(
    draw,
    max_bus_count=16,
    calculation_rates=((CalculationRate.AUDIO, CalculationRate.CONTROL)),
) -> SampleBusGroup:

    bus_count = draw(st.integers(min_value=1, max_value=max_bus_count))
    calculation_rate = draw(st.sampled_from(calculation_rates))
    bus_group = supriya.realtime.BusGroup(
        bus_count=bus_count, calculation_rate=calculation_rate
    )

    sample = SampleBusGroup(bus_group, calculation_rate, bus_count)
    sample.set_values = tuple(
        draw(st.floats(width=32, allow_infinity=False, allow_nan=False))
        for _ in range(bus_count)
    )

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus_group())
def test_allocate_01(server, strategy):

    control, test = strategy

    for sample in control:
        assert not sample.bus_group.is_allocated
        assert sample.bus_group.bus_id is None
        assert sample.bus_group.server is None
        for bus in sample.bus_group:
            assert not bus.is_allocated
            assert bus.bus_group is sample.bus_group
            assert bus.bus_id is None
            assert bus.calculation_rate == sample.calculation_rate

    bus_control_count = 0
    bus_audio_count = server.options.first_private_bus_id
    for sample in test:
        sample.bus_group.allocate(server)
        assert sample.bus_group.is_allocated
        assert sample.bus_group.server is server
        if sample.calculation_rate == CalculationRate.CONTROL:
            assert sample.bus_group.bus_id == bus_control_count
            assert sample.bus_group.map_symbol == f"c{bus_control_count}"
            bus_control_count += sample.bus_count
        if sample.calculation_rate == CalculationRate.AUDIO:
            assert sample.bus_group.bus_id == bus_audio_count
            assert sample.bus_group.map_symbol == f"a{bus_audio_count}"
            bus_audio_count += sample.bus_count
        for i, bus in enumerate(sample.bus_group):
            assert bus.is_allocated
            assert bus.bus_group is sample.bus_group
            assert bus.calculation_rate == sample.calculation_rate
            assert bus.bus_id == sample.bus_group.bus_id + i
            assert sample.bus_group.index(bus) == i
    assert all(_.bus_group.is_allocated for _ in test)
    assert all(_.bus_group.free() for _ in test)
    assert not any(_.bus_group.is_allocated for _ in test)

    for sample in control:
        assert not sample.bus_group.is_allocated
        assert sample.bus_group.bus_id is None
        assert sample.bus_group.server is None
        for bus in sample.bus_group:
            assert not bus.is_allocated
            assert bus.bus_group is sample.bus_group
            assert bus.bus_id is None
            assert bus.calculation_rate == sample.calculation_rate


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus_group(calculation_rates=("control",)))
def test_getset(server, strategy):

    control, test = strategy

    assert all(_.bus_group.allocate(server) for _ in control + test)
    assert all(_.bus_group.is_allocated for _ in control + test)
    control_vals = tuple(_.bus_group.get() for _ in control)

    for sample in test:
        sample.bus_group.set(*sample.set_values)
        results = sample.bus_group.get()
        assert results == sample.set_values

    assert control_vals == tuple(_.bus_group.get() for _ in control)
    assert all(_.bus_group.free() for _ in control + test)
    assert not any(_.bus_group.is_allocated for _ in control + test)


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus_group(calculation_rates=("control",)))
def test_fill(server, strategy):

    control, test = strategy

    assert all(_.bus_group.allocate(server) for _ in control + test)
    assert all(_.bus_group.is_allocated for _ in control + test)
    control_vals = tuple(_.bus_group.get() for _ in control)

    for sample in test:
        val = sample.set_values[0]
        sample.bus_group.fill(val)
        results = sample.bus_group.get()
        assert results == tuple(val for _ in range(sample.bus_count))

    assert control_vals == tuple(_.bus_group.get() for _ in control)
    assert all(_.bus_group.free() for _ in control + test)
    assert not any(_.bus_group.is_allocated for _ in control + test)


def test_exceptions(server):

    with pytest.raises(ValueError):
        _ = supriya.realtime.BusGroup(calculation_rate="REALLYFAST")  # type: ignore
    with pytest.raises(ValueError):
        _ = supriya.realtime.BusGroup(bus_count=-0.01)  # type: ignore
    with pytest.raises(ValueError):
        _ = supriya.realtime.BusGroup(bus_id={})

    bus_group = supriya.realtime.BusGroup(calculation_rate=CalculationRate.CONTROL)
    with pytest.raises(BusNotAllocated):
        bus_group.fill(0.0)
    with pytest.raises(BusNotAllocated):
        _ = bus_group.get()
    with pytest.raises(BusNotAllocated):
        bus_group.set(*[0.0 for _ in range(len(bus_group))])

    bus_group = supriya.realtime.BusGroup(calculation_rate=CalculationRate.AUDIO)
    bus_group.allocate(server)
    assert bus_group.is_allocated
    with pytest.raises(IncompatibleRate):
        bus_group.fill(0.0)
    with pytest.raises(IncompatibleRate):
        _ = bus_group.get()
    with pytest.raises(IncompatibleRate):
        bus_group.set(*[0.0 for _ in range(len(bus_group))])
    bus_group.free()
    assert not bus_group.is_allocated
