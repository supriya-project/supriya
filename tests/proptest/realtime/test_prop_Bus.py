from dataclasses import dataclass
from typing import Optional

import hypothesis
import hypothesis.strategies as st
import pytest

import supriya.assets
import supriya.realtime
import supriya.synthdefs
from supriya import CalculationRate
from supriya.exceptions import BusAlreadyAllocated, BusNotAllocated, IncompatibleRate
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
class SampleBus:
    bus: supriya.realtime.Bus
    calculation_rate: CalculationRate
    bus_group_or_index: Optional[int] = None
    set_value: float = 0.0
    bus_index_min: int = 0
    bus_index_max: int = 16383


@get_control_test_groups(max_size=64)
@st.composite
def st_bus(
    draw,
    calculation_rates=((CalculationRate.AUDIO, CalculationRate.CONTROL)),
    user_id: bool = False,
) -> SampleBus:

    if user_id:
        bus_group_or_index = draw(
            st.integers(
                min_value=SampleBus.bus_index_min, max_value=SampleBus.bus_index_max
            )
        )
    else:
        bus_group_or_index = None
    calculation_rate = draw(st.sampled_from(calculation_rates))
    bus = supriya.realtime.Bus(
        bus_group_or_index=bus_group_or_index, calculation_rate=calculation_rate
    )
    sample = SampleBus(bus, calculation_rate)

    sample.set_value = draw(st.floats(width=32, allow_infinity=False, allow_nan=False))
    sample.bus_group_or_index = bus_group_or_index

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus())
def test_allocate_01(server, strategy):

    control, test = strategy

    for sample in control:
        assert sample.bus.bus_group is None
        assert sample.bus.calculation_rate == sample.calculation_rate
        assert not sample.bus.is_allocated
        assert sample.bus.server is None
        assert sample.bus.bus_id is None

    assert all(_.bus.allocate(server) for _ in test)
    bus_audio_count = 0
    bus_control_count = 0
    for sample in test:
        assert sample.bus.is_allocated
        assert sample.bus.calculation_rate == sample.calculation_rate
        assert sample.bus.server == server
        if sample.calculation_rate == CalculationRate.CONTROL:
            assert sample.bus.bus_id == bus_control_count
            assert sample.bus.map_symbol == f"c{bus_control_count}"
            assert int(sample.bus) == bus_control_count
            assert float(sample.bus) == float(bus_control_count)
            bus_control_count += 1
        if sample.calculation_rate == CalculationRate.AUDIO:
            first_audio_bus = server.options.first_private_bus_id
            assert sample.bus.bus_id == bus_audio_count + first_audio_bus
            assert sample.bus.map_symbol == f"a{bus_audio_count+first_audio_bus}"
            assert int(sample.bus) == bus_audio_count + first_audio_bus
            assert float(sample.bus) == float(bus_audio_count + first_audio_bus)
            bus_audio_count += 1
    assert all(_.bus.free() for _ in test)
    assert not any(_.bus.is_allocated for _ in test)
    for sample in test:
        assert sample.bus.bus_group is None
        assert sample.bus.calculation_rate == sample.calculation_rate
        assert not sample.bus.is_allocated
        assert sample.bus.server is None
        assert sample.bus.bus_id is None

    for sample in control:
        assert sample.bus.bus_group is None
        assert sample.bus.calculation_rate == sample.calculation_rate
        assert not sample.bus.is_allocated
        assert sample.bus.server is None
        assert sample.bus.bus_id is None


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus(user_id=True))
def test_allocate_02(server, strategy):

    control, test = strategy

    for sample in control:
        assert sample.bus.bus_id == sample.bus_group_or_index
        assert not sample.bus.is_allocated
        assert sample.bus.server is None
        assert sample.bus.bus_group is None

    for sample in test:
        sample.bus.allocate(server)
        assert sample.bus.bus_id == sample.bus_group_or_index
        assert sample.bus.is_allocated
        assert sample.bus.server is server
        assert sample.bus.bus_group is None
        sample.bus.free()
        assert sample.bus.bus_id is None
        assert not sample.bus.is_allocated
        assert sample.bus.server is None
        assert sample.bus.bus_group is None
    server.sync()

    for sample in control:
        assert sample.bus.bus_id == sample.bus_group_or_index
        assert not sample.bus.is_allocated
        assert sample.bus.server is None
        assert sample.bus.bus_group is None


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus(calculation_rates=(CalculationRate.CONTROL,)))
def test_getset(server, strategy):

    control, test = strategy

    assert all(_.bus.allocate(server) for _ in control + test)
    assert all(_.bus.is_allocated for _ in control + test)
    control_vals = tuple(_.bus.get() for _ in control)

    for sample in test:
        sample.bus.set(sample.set_value)
        assert sample.bus.get() == sample.set_value
        assert sample.bus.value == sample.set_value

    assert control_vals == tuple(_.bus.get() for _ in control)
    assert all(_.bus.free() for _ in control + test)
    assert not any(_.bus.is_allocated for _ in control + test)


def test_exceptions(server):

    bus = supriya.realtime.Bus(calculation_rate="control")
    with pytest.raises(BusNotAllocated):
        _ = bus.map_symbol
    with pytest.raises(BusNotAllocated):
        _ = float(bus)
    with pytest.raises(BusNotAllocated):
        _ = int(bus)
    with pytest.raises(ValueError):
        supriya.realtime.Bus(calculation_rate="REALLYFAST")

    buses = []
    for _ in range(
        server.options.audio_bus_channel_count - server.options.first_private_bus_id
    ):
        bus = supriya.realtime.Bus(calculation_rate="audio")
        bus.allocate(server)
        buses.append(bus)
    with pytest.raises(ValueError):
        bus = supriya.realtime.Bus(calculation_rate="audio")
        bus.allocate(server)
    for bus in buses:
        bus.free()
    server.sync()

    for rate in ("control", "audio"):
        bus = supriya.realtime.Bus(calculation_rate=rate)
        with pytest.raises(BusNotAllocated):
            bus.free()
        bus.allocate(server)
        assert bus.is_allocated
        with pytest.raises(BusAlreadyAllocated):
            bus.allocate(server)
        bus.free()
        assert not bus.is_allocated
        server.sync()

    bus = supriya.realtime.Bus()
    assert not bus.value
    with pytest.raises(BusNotAllocated):
        _ = bus.get()
    with pytest.raises(BusNotAllocated):
        bus.set(0.0)

    bus = supriya.realtime.Bus(calculation_rate="audio")
    bus.allocate(server)
    assert bus.is_allocated
    with pytest.raises(IncompatibleRate):
        _ = bus.get()
    with pytest.raises(IncompatibleRate):
        bus.set(0.0)
    bus.free()
    assert not bus.is_allocated


@pytest.mark.parametrize(
    "rate_params",
    [
        (None, CalculationRate.CONTROL),
        (CalculationRate.CONTROL, CalculationRate.CONTROL),
        ("control", CalculationRate.CONTROL),
        (CalculationRate.AUDIO, CalculationRate.AUDIO),
        ("audio", CalculationRate.AUDIO),
    ],
)
def test_server_add_bus(server, rate_params):

    rate_arg, rate = rate_params
    bus = server.add_bus(calculation_rate=rate_arg)
    assert bus.is_allocated
    assert bus.calculation_rate == rate
    bus.free()
    assert not bus.is_allocated

    with pytest.raises(ValueError):
        bus = server.add_bus(calculation_rate="REALLYFAST")
