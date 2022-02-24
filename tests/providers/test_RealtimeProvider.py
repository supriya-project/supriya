import time

import pytest
from uqbar.strings import normalize

from supriya.assets.synthdefs import default
from supriya.enums import AddAction, CalculationRate
from supriya.providers import (
    BufferProxy,
    BusGroupProxy,
    BusProxy,
    GroupProxy,
    Provider,
    ProviderMoment,
    RealtimeProvider,
    SynthProxy,
)
from supriya.utils import locate


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(default)
    yield persistent_server


def test_RealtimeProvider_init_error():
    with pytest.raises(ValueError):
        RealtimeProvider(23)


def test_RealtimeProvider_add_buffer_1(server):
    provider = Provider.from_context(server)
    file_path = locate("supriya.assets:audio/pulse_44100sr_16bit_octo.wav")
    with server.osc_protocol.capture() as transcript:
        with provider.at(1.2345):
            proxy = provider.add_buffer(file_path=file_path)
        time.sleep(0.1)
    assert isinstance(proxy, BufferProxy)
    assert [entry.message.to_list() for entry in transcript] == [
        [1.3345, [["/b_allocRead", 0, str(file_path), 0, -1]]],
        ["/done", "/b_allocRead", 0],
    ]


def test_RealtimeProvider_add_bus_1(server):
    provider = Provider.from_context(server)
    with provider.at(1.2345):
        bus_proxy_one = provider.add_bus(calculation_rate="audio")
        bus_proxy_two = provider.add_bus()
    assert bus_proxy_one == BusProxy(
        calculation_rate=CalculationRate.AUDIO, identifier=16, provider=provider
    )
    assert bus_proxy_two == BusProxy(
        calculation_rate=CalculationRate.CONTROL, identifier=0, provider=provider
    )


def test_RealtimeProvider_add_bus_error(server):
    """
    Must be control or audio rate.
    """
    provider = Provider.from_context(server)
    with pytest.raises(ValueError):
        provider.add_bus()
    with provider.at(0):
        with pytest.raises(ValueError):
            provider.add_bus(calculation_rate="scalar")


def test_RealtimeProvider_add_bus_group_1(server):
    provider = Provider.from_context(server)
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            bus_group_proxy_one = provider.add_bus_group(channel_count=2)
            bus_group_proxy_two = provider.add_bus_group(channel_count=4)
    assert bus_group_proxy_one == BusGroupProxy(
        calculation_rate=CalculationRate.CONTROL,
        channel_count=2,
        identifier=0,
        provider=provider,
    )
    assert bus_group_proxy_two == BusGroupProxy(
        calculation_rate=CalculationRate.CONTROL,
        channel_count=4,
        identifier=2,
        provider=provider,
    )
    assert [entry.message for entry in transcript] == []


def test_RealtimeProvider_add_bus_group_error(server):
    """
    Must be 1 or more channels and control or audio rate.
    """
    provider = Provider.from_context(server)
    with pytest.raises(ValueError):
        provider.add_bus_group()
    with provider.at(0):
        with pytest.raises(ValueError):
            provider.add_bus_group(channel_count=0)
        with pytest.raises(ValueError):
            provider.add_bus_group(calculation_rate="scalar")


def test_RealtimeProvider_add_group_1(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(seconds) as provider_moment:
            group_proxy = provider.add_group()
    assert group_proxy == GroupProxy(identifier=1000, provider=provider)
    assert provider_moment == ProviderMoment(
        provider=provider,
        seconds=seconds,
        bus_settings=[],
        node_additions=[(group_proxy, AddAction.ADD_TO_HEAD, server.default_group)],
        node_removals=[],
        node_reorderings=[],
        node_settings=[],
    )
    assert [entry.message.to_list() for entry in transcript] == [
        [seconds + provider.latency, [["/g_new", 1000, 0, 1]]]
    ]
    time.sleep(0.1)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
    """
    )


def test_RealtimeProvider_add_group_2(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            group_proxy_one = provider.add_group()
        with provider.at(seconds + 0.01) as provider_moment:
            group_proxy_two = provider.add_group(target_node=group_proxy_one)
    assert group_proxy_two == GroupProxy(identifier=1001, provider=provider)
    assert provider_moment == ProviderMoment(
        provider=provider,
        seconds=seconds + 0.01,
        bus_settings=[],
        node_additions=[(group_proxy_two, AddAction.ADD_TO_HEAD, group_proxy_one)],
        node_removals=[],
        node_reorderings=[],
        node_settings=[],
    )
    assert [entry.message.to_list() for entry in transcript] == [
        [None, [["/g_new", 1000, 0, 1]]],
        [seconds + 0.01 + provider.latency, [["/g_new", 1001, 0, 1000]]],
    ]
    time.sleep(0.1)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 group
        """
    )


def test_RealtimeProvider_add_group_error(server):
    """
    Requires moment.
    """
    provider = Provider.from_context(server)
    with pytest.raises(ValueError):
        provider.add_group()


def test_RealtimeProvider_add_synth_1(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(seconds) as provider_moment:
            synth_proxy = provider.add_synth(amplitude=0.3, frequency=333)
    assert synth_proxy == SynthProxy(
        identifier=1000,
        provider=provider,
        synthdef=default,
        settings=dict(amplitude=0.3, frequency=333),
    )
    assert provider_moment == ProviderMoment(
        provider=provider,
        seconds=seconds,
        bus_settings=[],
        node_additions=[(synth_proxy, AddAction.ADD_TO_HEAD, server.default_group)],
        node_removals=[],
        node_reorderings=[],
        node_settings=[],
    )
    assert [entry.message.to_list() for entry in transcript] == [
        [
            seconds + provider.latency,
            [["/s_new", "default", 1000, 0, 1, "amplitude", 0.3, "frequency", 333]],
        ]
    ]
    time.sleep(0.1)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.3, frequency: 333.0, gate: 1.0, pan: 0.5
        """
    )


def test_RealtimeProvider_add_synth_2(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            group_proxy = provider.add_group()
        with provider.at(seconds + 0.01) as provider_moment:
            synth_proxy = provider.add_synth(
                target_node=group_proxy, amplitude=0.5, frequency=666
            )
    assert synth_proxy == SynthProxy(
        identifier=1001,
        provider=provider,
        synthdef=default,
        settings=dict(amplitude=0.5, frequency=666),
    )
    assert provider_moment == ProviderMoment(
        provider=provider,
        seconds=seconds + 0.01,
        bus_settings=[],
        node_additions=[(synth_proxy, AddAction.ADD_TO_HEAD, group_proxy)],
        node_removals=[],
        node_reorderings=[],
        node_settings=[],
    )
    assert [entry.message.to_list() for entry in transcript] == [
        [None, [["/g_new", 1000, 0, 1]]],
        [
            seconds + 0.01 + provider.latency,
            [["/s_new", "default", 1001, 0, 1000, "amplitude", 0.5, "frequency", 666]],
        ],
    ]
    time.sleep(0.1)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 default
                        out: 0.0, amplitude: 0.5, frequency: 666.0, gate: 1.0, pan: 0.5
        """
    )


def test_RealtimeProvider_add_synth_3(server):
    provider = Provider.from_context(server)
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            audio_bus_proxy = provider.add_bus("audio")
            control_bus_proxy = provider.add_bus("control")
            synth_proxy = provider.add_synth(
                amplitude=control_bus_proxy, out=audio_bus_proxy
            )
    assert synth_proxy == SynthProxy(
        identifier=1000,
        provider=provider,
        synthdef=default,
        settings=dict(amplitude=control_bus_proxy, out=audio_bus_proxy),
    )
    assert [entry.message.to_list() for entry in transcript] == [
        [None, [["/s_new", "default", 1000, 0, 1, "amplitude", "c0", "out", 16.0]]]
    ]
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 default
                    out: 16.0, amplitude: c0, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )


def test_RealtimeProvider_add_synth_error(server):
    """
    Requires moment.
    """
    provider = Provider.from_context(server)
    with pytest.raises(ValueError):
        provider.add_synth()


def test_RealtimeProvider_free_buffer(server):
    provider = Provider.from_context(server)
    file_path = locate("supriya.assets:audio/pulse_44100sr_16bit_octo.wav")
    with provider.at(1.2345):
        proxy = provider.add_buffer(file_path=file_path)
    time.sleep(0.1)
    with server.osc_protocol.capture() as transcript:
        with provider.at(2.3456):
            proxy.free()
    assert [entry.message.to_list() for entry in transcript] == [
        [2.4456, [["/b_free", 0]]]
    ]


def test_RealtimeProvider_free_bus_1(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(seconds):
            audio_bus = provider.add_bus(calculation_rate=CalculationRate.AUDIO)
            control_bus_a = provider.add_bus()
            control_bus_b = provider.add_bus()
            control_bus_c = provider.add_bus()
        with provider.at(seconds + 0.01):
            audio_bus.free()
            control_bus_a.free()
            control_bus_d = provider.add_bus()
    assert audio_bus.identifier == 16
    assert control_bus_a.identifier == 0
    assert control_bus_b.identifier == 1
    assert control_bus_c.identifier == 2
    assert control_bus_d.identifier == 0
    assert [entry.message for entry in transcript] == []


def test_RealtimeProvider_free_bus_error(server):
    provider = Provider.from_context(server)
    with provider.at(0):
        bus_proxy = provider.add_bus()
    with pytest.raises(ValueError):
        provider.free_bus(bus_proxy)


def test_RealtimeProvider_free_bus_group_1(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(seconds):
            audio_bus_group = provider.add_bus_group(
                channel_count=2, calculation_rate=CalculationRate.AUDIO
            )
            control_bus_group_a = provider.add_bus_group(channel_count=2)
            control_bus_group_b = provider.add_bus_group(channel_count=3)
            control_bus_group_c = provider.add_bus_group(channel_count=2)
        with provider.at(seconds + 0.01):
            audio_bus_group.free()
            control_bus_group_a.free()
            control_bus_group_d = provider.add_bus_group(channel_count=2)
    assert audio_bus_group.identifier == 16
    assert control_bus_group_a.identifier == 0
    assert control_bus_group_b.identifier == 2
    assert control_bus_group_c.identifier == 5
    assert control_bus_group_d.identifier == 0
    assert [entry.message for entry in transcript] == []


def test_RealtimeProvider_free_bus_group_error(server):
    provider = Provider.from_context(server)
    with provider.at(0):
        bus_group_proxy = provider.add_bus_group()
    with pytest.raises(ValueError):
        provider.free_bus_group(bus_group_proxy)


def test_RealtimeProvider_free_node_error(server):
    """
    Requires moment.
    """
    provider = Provider.from_context(server)
    with provider.at(0):
        group_proxy = provider.add_group()
    with pytest.raises(ValueError):
        provider.free_node(group_proxy)


def test_RealtimeProvider_free_node_1(server):
    provider = Provider.from_context(server)
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            group_proxy = provider.add_group()
            synth_proxy = provider.add_synth()
        with provider.at(None):
            group_proxy.free()
            synth_proxy.free()
    assert [entry.message.to_list() for entry in transcript] == [
        [None, [["/g_new", 1000, 0, 1], ["/s_new", "default", 1001, 0, 1]]],
        [None, [["/n_free", 1000], ["/n_set", 1001, "gate", 0]]],
    ]
    time.sleep(0.1)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 0.0, pan: 0.5
        """
    )


def test_RealtimeProvider_move_node_1(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(seconds):
            group_proxy_one = provider.add_group()
            group_proxy_two = provider.add_group()
            provider.move_node(group_proxy_one, AddAction.ADD_TO_TAIL, group_proxy_two)
    assert [entry.message.to_list() for entry in transcript] == [
        [
            seconds + provider.latency,
            [["/g_new", 1000, 0, 1], ["/g_new", 1001, 0, 1], ["/g_tail", 1001, 1000]],
        ]
    ]
    time.sleep(0.1)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1000 group
        """
    )


def test_RealtimeProvider_move_node_error(server):
    """
    Requires moment.
    """
    provider = Provider.from_context(server)
    with provider.at(0):
        group_proxy_one = provider.add_group()
        group_proxy_two = provider.add_group()
    with pytest.raises(ValueError):
        group_proxy_one.move(AddAction.ADD_TO_HEAD, group_proxy_two)


def test_RealtimeProvider_set_bus_1(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with server.osc_protocol.capture() as transcript:
        with provider.at(seconds):
            bus_group_proxy = provider.add_bus_group(channel_count=4)
            for i, bus_proxy in enumerate(bus_group_proxy):
                bus_proxy.set_(pow(2, i))
    assert [entry.message.to_list() for entry in transcript] == [
        [seconds + provider.latency, [["/c_set", 0, 1.0, 1, 2.0, 2, 4.0, 3, 8.0]]]
    ]


def test_RealtimeProvider_set_bus_error(server):
    provider = Provider.from_context(server)
    with provider.at(1.2345):
        audio_bus_proxy = provider.add_bus(calculation_rate=CalculationRate.AUDIO)
        control_bus_proxy = provider.add_bus()
        with pytest.raises(ValueError):
            audio_bus_proxy.set_(0.1234)
    with pytest.raises(ValueError):
        control_bus_proxy.set_(0.1234)


def test_RealtimeProvider_set_node_1(server):
    provider = Provider.from_context(server)
    seconds = time.time()
    with provider.at(seconds):
        group_proxy = provider.add_group()
    with server.osc_protocol.capture() as transcript:
        with provider.at(seconds + 0.01):
            group_proxy["foo"] = 23
    assert [entry.message.to_list() for entry in transcript] == [
        [seconds + 0.01 + provider.latency, [["/n_set", 1000, "foo", 23]]]
    ]


def test_RealtimeProvider_set_node_2(server):
    provider = Provider.from_context(server)
    with provider.at(None):
        synth_proxy = provider.add_synth()
    time.sleep(0.01)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
        """
    )
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            synth_proxy["frequency"] = 443
    assert [entry.message.to_list() for entry in transcript] == [
        [None, [["/n_set", 1000, "frequency", 443.0]]]
    ]
    time.sleep(0.01)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: 443.0, gate: 1.0, pan: 0.5
        """
    )


def test_RealtimeProvider_set_node_3(server):
    provider = Provider.from_context(server)
    with provider.at(None):
        synth_proxy = provider.add_synth()
        bus_proxy = provider.add_bus()
    time.sleep(0.01)
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            synth_proxy["frequency"] = bus_proxy
    assert [
        entry.message.to_list()
        for entry in transcript
        if not (entry.label == "R" and entry.message.address == "/status.reply")
    ] == [[None, [["/n_set", 1000, "frequency", "c0"]]]]
    time.sleep(0.01)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: c0, gate: 1.0, pan: 0.5
        """
    )
    time.sleep(0.01)
    with server.osc_protocol.capture() as transcript:
        with provider.at(None):
            synth_proxy["frequency"] = 443
    assert [
        entry.message.to_list()
        for entry in transcript
        if not (entry.label == "R" and entry.message.address == "/status.reply")
    ] == [[None, [["/n_set", 1000, "frequency", 443.0]]]]
    time.sleep(0.01)
    assert str(server.query()) == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: 443.0, gate: 1.0, pan: 0.5
        """
    )


def test_RealtimeProvider_set_node_error(server):
    provider = Provider.from_context(server)
    with provider.at(None):
        group_proxy = provider.add_group()
        synth_proxy = provider.add_synth()
    with pytest.raises(ValueError):
        group_proxy["foo"] = 23
    with pytest.raises(ValueError):
        synth_proxy["foo"] = 23
