import pytest

from supriya.assets.synthdefs import default
from supriya.enums import AddAction, CalculationRate
from supriya.providers import (
    BufferProxy,
    BusGroupProxy,
    BusProxy,
    GroupProxy,
    NonrealtimeProvider,
    Provider,
    SynthProxy,
)
from supriya.utils import locate


def test_NonrealtimeProvider_init_error():
    with pytest.raises(ValueError):
        NonrealtimeProvider(23)


def test_NonrealtimeProvider_add_buffer_1(session):
    provider = Provider.from_context(session)
    file_path = locate("supriya.assets:audio/pulse_44100sr_16bit_octo.wav")
    with provider.at(1.2345):
        proxy = provider.add_buffer(file_path=file_path)
    assert isinstance(proxy, BufferProxy)
    assert session.to_lists(10) == [
        [1.2345, [["/b_allocRead", 0, str(file_path), 0, -1]]],
        [10.0, [["/b_free", 0], [0]]],
    ]


def test_NonrealtimeProvider_add_bus_1(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        bus_proxy_one = provider.add_bus(calculation_rate="audio")
        bus_proxy_two = provider.add_bus()
    assert bus_proxy_one == BusProxy(
        calculation_rate=CalculationRate.AUDIO,
        identifier=session.buses_by_session_id[0],
        provider=provider,
    )
    assert bus_proxy_two == BusProxy(
        calculation_rate=CalculationRate.CONTROL,
        identifier=session.buses_by_session_id[1],
        provider=provider,
    )
    assert session.to_lists(10) == [[10.0, [[0]]]]


def test_NonrealtimeProvider_add_bus_error(session):
    """
    Must be control or audio rate.
    """
    provider = Provider.from_context(session)
    with pytest.raises(ValueError):
        provider.add_bus()
    with provider.at(0):
        with pytest.raises(ValueError):
            provider.add_bus(calculation_rate="scalar")


def test_NonrealtimeProvider_add_bus_group_1(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        bus_group_proxy_one = provider.add_bus_group(channel_count=2)
        bus_group_proxy_two = provider.add_bus_group(channel_count=4)
    assert bus_group_proxy_one == BusGroupProxy(
        calculation_rate=CalculationRate.CONTROL,
        channel_count=2,
        identifier=session.buses_by_session_id[0],
        provider=provider,
    )
    assert bus_group_proxy_two == BusGroupProxy(
        calculation_rate=CalculationRate.CONTROL,
        channel_count=4,
        identifier=session.buses_by_session_id[1],
        provider=provider,
    )
    assert session.to_lists(10) == [[10.0, [[0]]]]


def test_NonrealtimeProvider_add_bus_group_error(session):
    """
    Must be 1 or more channels and control or audio rate.
    """
    provider = Provider.from_context(session)
    with pytest.raises(ValueError):
        provider.add_bus_group()
    with provider.at(0):
        with pytest.raises(ValueError):
            provider.add_bus_group(channel_count=0)
        with pytest.raises(ValueError):
            provider.add_bus_group(calculation_rate="scalar")


def test_NonrealtimeProvider_add_group_1(session):
    provider = Provider.from_context(session)
    seconds = 1.2345
    with provider.at(seconds):
        group_proxy = provider.add_group()
    assert group_proxy == GroupProxy(
        identifier=session.nodes_by_session_id[1000], provider=provider
    )
    assert session.to_lists(10) == [
        [1.2345, [["/g_new", 1000, 0, 0]]],
        [10.0, [["/n_free", 1000], [0]]],
    ]


def test_NonrealtimeProvider_add_group_2(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        group_proxy_one = provider.add_group()
    with provider.at(2.3456):
        group_proxy_two = provider.add_group(target_node=group_proxy_one)
    assert session.to_lists(10) == [
        [1.2345, [["/g_new", 1000, 0, 0]]],
        [2.3456, [["/g_new", 1001, 0, 1000]]],
        [10.0, [["/n_free", 1000, 1001], [0]]],
    ]
    assert group_proxy_one == GroupProxy(
        identifier=session.nodes_by_session_id[1000], provider=provider
    )
    assert group_proxy_two == GroupProxy(
        identifier=session.nodes_by_session_id[1001], provider=provider
    )


def test_NonrealtimeProvider_add_group_error(session):
    """
    Requires moment.
    """
    provider = Provider.from_context(session)
    with pytest.raises(ValueError):
        provider.add_group()


def test_NonrealtimeProvider_add_synth_1(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        synth_proxy = provider.add_synth(amplitude=0.3, frequency=333)
    assert synth_proxy == SynthProxy(
        identifier=session.nodes_by_session_id[1000],
        provider=provider,
        synthdef=default,
        settings=dict(amplitude=0.3, frequency=333),
    )
    assert session.to_lists(10) == [
        [
            1.2345,
            [
                *pytest.helpers.build_d_recv_commands([default]),
                [
                    "/s_new",
                    default.anonymous_name,
                    1000,
                    0,
                    0,
                    "amplitude",
                    0.3,
                    "frequency",
                    333,
                ],
            ],
        ],
        [10.0, [["/n_set", 1000, "gate", 0], [0]]],
    ]


def test_NonrealtimeProvider_add_synth_2(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        group_proxy = provider.add_group()
    with provider.at(2.3456):
        synth_proxy = provider.add_synth(
            target_node=group_proxy, amplitude=0.5, frequency=666
        )
    assert synth_proxy == SynthProxy(
        identifier=session.nodes_by_session_id[1001],
        provider=provider,
        synthdef=default,
        settings=dict(amplitude=0.5, frequency=666),
    )
    assert session.to_lists(10) == [
        [1.2345, [["/g_new", 1000, 0, 0]]],
        [
            2.3456,
            [
                *pytest.helpers.build_d_recv_commands([default]),
                [
                    "/s_new",
                    default.anonymous_name,
                    1001,
                    0,
                    1000,
                    "amplitude",
                    0.5,
                    "frequency",
                    666,
                ],
            ],
        ],
        [10.0, [["/n_free", 1000], ["/n_set", 1001, "gate", 0], [0]]],
    ]


def test_NonrealtimeProvider_add_synth_error(session):
    """
    Requires moment.
    """
    provider = Provider.from_context(session)
    with pytest.raises(ValueError):
        provider.add_synth()


@pytest.mark.skip("NRT doesn't implement freeing buffers")
def test_NonrealtimeProvider_free_buffer(session):
    ...


def test_NonrealtimeProvider_free_bus(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        bus_proxy = provider.add_bus()
    with provider.at(2.3456):
        provider.free_bus(bus_proxy)
    assert session.to_lists(10) == [[10.0, [[0]]]]


def test_NonrealtimeProvider_free_bus_error(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        bus_proxy = provider.add_bus()
    with pytest.raises(ValueError):
        provider.free_bus(bus_proxy)


def test_NonrealtimeProvider_free_bus_group(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        bus_group_proxy = provider.add_bus_group(channel_count=2)
    with provider.at(2.3456):
        bus_group_proxy.free()
    assert session.to_lists(10) == [[10.0, [[0]]]]


def test_NonrealtimeProvider_free_bus_group_error(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        bus_group_proxy = provider.add_bus_group(channel_count=2)
    with pytest.raises(ValueError):
        bus_group_proxy.free()


def test_NonrealtimeProvider_free_node_1(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        group_proxy = provider.add_group()
        synth_proxy = provider.add_synth()
    with provider.at(2.3456):
        group_proxy.free()
        synth_proxy.free()
    assert session.to_lists(10) == [
        [
            1.2345,
            [
                *pytest.helpers.build_d_recv_commands([default]),
                ["/g_new", 1000, 0, 0],
                ["/s_new", default.anonymous_name, 1001, 0, 0],
            ],
        ],
        [2.3456, [["/n_free", 1000], ["/n_set", 1001, "gate", 0]]],
        [10.0, [[0]]],
    ]


def test_NonrealtimeProvider_free_node_error(session):
    """
    Requires moment.
    """
    provider = Provider.from_context(session)
    with provider.at(0):
        group_proxy = provider.add_group()
    with pytest.raises(ValueError):
        provider.free_node(group_proxy)


def test_NonrealtimeProvider_move_node_1(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        group_proxy_one = provider.add_group()
        group_proxy_two = provider.add_group()
    with provider.at(2.3456):
        provider.move_node(group_proxy_one, AddAction.ADD_TO_TAIL, group_proxy_two)
    assert session.to_lists(10) == [
        [1.2345, [["/g_new", 1000, 0, 0], ["/g_new", 1001, 0, 0]]],
        [2.3456, [["/g_tail", 1001, 1000]]],
        [10.0, [["/n_free", 1000, 1001], [0]]],
    ]


def test_NonrealtimeProvider_move_node_error(session):
    """
    Requires moment.
    """
    provider = Provider.from_context(session)
    with provider.at(0):
        group_proxy_one = provider.add_group()
        group_proxy_two = provider.add_group()
    with pytest.raises(ValueError):
        group_proxy_one.move(AddAction.ADD_TO_HEAD, group_proxy_two)


def test_NonrealtimeProvider_set_bus_1(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        bus_group_proxy = provider.add_bus_group(channel_count=4)
        for i, bus_proxy in enumerate(bus_group_proxy):
            bus_proxy.set_(pow(2, i))
    assert session.to_lists(10) == [
        [1.2345, [["/c_set", 0, 1.0, 1, 2.0, 2, 4.0, 3, 8.0]]],
        [10.0, [[0]]],
    ]


def test_NonrealtimeProvider_set_bus_error(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        audio_bus_proxy = provider.add_bus(calculation_rate=CalculationRate.AUDIO)
        control_bus_proxy = provider.add_bus()
        with pytest.raises(ValueError):
            audio_bus_proxy.set_(0.1234)
    with pytest.raises(ValueError):
        control_bus_proxy.set_(0.1234)


def test_NonrealtimeProvider_set_node_1(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        group_proxy = provider.add_group()
    with provider.at(2.3456):
        group_proxy["foo"] = 23
    assert session.to_lists(10) == [
        [1.2345, [["/g_new", 1000, 0, 0]]],
        [2.3456, [["/n_set", 1000, "foo", 23]]],
        [10.0, [["/n_free", 1000], [0]]],
    ]


def test_NonrealtimeProvider_set_node_2(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        synth_proxy = provider.add_synth()
    with provider.at(2.3456):
        synth_proxy["frequency"] = 666.666
    assert session.to_lists(10) == [
        [
            1.2345,
            [
                *pytest.helpers.build_d_recv_commands([default]),
                ["/s_new", default.anonymous_name, 1000, 0, 0],
            ],
        ],
        [2.3456, [["/n_set", 1000, "frequency", 666.666]]],
        [10.0, [["/n_set", 1000, "gate", 0], [0]]],
    ]


def test_NonrealtimeProvider_set_node_3(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        synth_proxy = provider.add_synth()
        bus_proxy = provider.add_bus()
    with provider.at(2.3456):
        synth_proxy["frequency"] = bus_proxy
    with provider.at(3.4567):
        synth_proxy["frequency"] = 443
    assert session.to_lists(10) == [
        [
            1.2345,
            [
                *pytest.helpers.build_d_recv_commands([default]),
                ["/s_new", default.anonymous_name, 1000, 0, 0],
            ],
        ],
        [2.3456, [["/n_set", 1000, "frequency", "c0"]]],
        [3.4567, [["/n_set", 1000, "frequency", 443.0]]],
        [10.0, [["/n_set", 1000, "gate", 0], [0]]],
    ]


def test_NonrealtimeProvider_set_node_error(session):
    provider = Provider.from_context(session)
    with provider.at(1.2345):
        group_proxy = provider.add_group()
        synth_proxy = provider.add_synth()
    with pytest.raises(ValueError):
        group_proxy["foo"] = 23
    with pytest.raises(ValueError):
        synth_proxy["foo"] = 23
